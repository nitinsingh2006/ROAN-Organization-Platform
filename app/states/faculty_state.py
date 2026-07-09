import reflex as rx
from typing import TypedDict
from datetime import datetime
from app.states.auth_state import AuthState
from app.data import seed
import logging


class StudentDirEntry(TypedDict):
    id: int
    full_name: str
    email: str
    enrolled_courses: str


class AttendanceRow(TypedDict):
    student_id: int
    student_name: str
    status: str


class AssessmentEntry(TypedDict):
    id: int
    student_name: str
    course_title: str
    title: str
    marks: float
    max_marks: float
    remarks: str


class PracticalEntry(TypedDict):
    id: int
    student_name: str
    course_title: str
    title: str
    grade: str
    remarks: str


class FacultyState(rx.State):
    status: str = ""
    error: str = ""
    search_query: str = ""
    selected_course_id: int = 0
    attendance_date: str = ""

    @rx.event
    def set_search(self, v: str):
        self.search_query = v

    @rx.event
    def set_course(self, v: str):
        try:
            self.selected_course_id = int(v)
        except Exception:
            logging.exception("Unexpected error")
            self.selected_course_id = 0

    @rx.event
    def set_date(self, v: str):
        self.attendance_date = v

    @rx.event
    def init_defaults(self):
        if self.attendance_date == "":
            self.attendance_date = datetime.utcnow().strftime("%Y-%m-%d")
        if self.selected_course_id == 0 and seed.COURSES:
            self.selected_course_id = seed.COURSES[0]["id"]

    @rx.var
    def course_options(self) -> list[dict[str, str]]:
        return [{"id": str(c["id"]), "title": c["title"]} for c in seed.COURSES]

    @rx.var
    def dashboard_metrics(self) -> dict[str, int]:
        return {
            "students": len(seed.all_students()),
            "courses": len(seed.COURSES),
            "attendance_records": len(seed.ATTENDANCE),
            "assessments": len(seed.ASSESSMENTS),
            "practicals": len(seed.PRACTICALS),
        }

    @rx.var
    def directory(self) -> list[StudentDirEntry]:
        q = self.search_query.lower().strip()
        out: list[StudentDirEntry] = []
        for u in seed.all_students():
            course_ids = seed.student_active_course_ids(u["id"])
            titles = [
                (
                    seed.find_course(cid)["title"]
                    if seed.find_course(cid)
                    else ""
                )
                for cid in course_ids
            ]
            entry: StudentDirEntry = {
                "id": u["id"],
                "full_name": u["full_name"],
                "email": u["email"],
                "enrolled_courses": ", ".join([t for t in titles if t]) or "—",
            }
            if (
                q == ""
                or q in u["full_name"].lower()
                or q in u["email"].lower()
            ):
                out.append(entry)
        return out

    @rx.var
    def attendance_roster(self) -> list[AttendanceRow]:
        if self.selected_course_id == 0:
            return []
        cid = self.selected_course_id
        date = self.attendance_date or datetime.utcnow().strftime("%Y-%m-%d")
        student_ids = [
            e["student_id"]
            for e in seed.ENROLLMENTS
            if e["course_id"] == cid and e["status"] == "active"
        ]
        existing = {
            a["student_id"]: a["status"]
            for a in seed.ATTENDANCE
            if a["course_id"] == cid and a["date"] == date
        }
        out: list[AttendanceRow] = []
        for sid in student_ids:
            u = seed.find_user_by_id(sid)
            if u is None:
                continue
            out.append(
                {
                    "student_id": sid,
                    "student_name": u["full_name"],
                    "status": existing.get(sid, "unmarked"),
                }
            )
        return out

    @rx.var
    def recent_assessments(self) -> list[AssessmentEntry]:
        out: list[AssessmentEntry] = []
        for a in list(reversed(seed.ASSESSMENTS))[:20]:
            u = seed.find_user_by_id(a["student_id"])
            c = seed.find_course(a["course_id"])
            out.append(
                {
                    "id": a["id"],
                    "student_name": u["full_name"] if u else "Unknown",
                    "course_title": c["title"] if c else "",
                    "title": a["title"],
                    "marks": a["marks"],
                    "max_marks": a["max_marks"],
                    "remarks": a["remarks"],
                }
            )
        return out

    @rx.var
    def recent_practicals(self) -> list[PracticalEntry]:
        out: list[PracticalEntry] = []
        for p in list(reversed(seed.PRACTICALS))[:20]:
            u = seed.find_user_by_id(p["student_id"])
            c = seed.find_course(p["course_id"])
            out.append(
                {
                    "id": p["id"],
                    "student_name": u["full_name"] if u else "Unknown",
                    "course_title": c["title"] if c else "",
                    "title": p["title"],
                    "grade": p["grade"],
                    "remarks": p["remarks"],
                }
            )
        return out

    async def _faculty_id(self) -> int:
        auth = await self.get_state(AuthState)
        return auth.user_id

    @rx.event
    async def mark_attendance(self, student_id: int, status: str):
        fid = await self._faculty_id()
        date = self.attendance_date or datetime.utcnow().strftime("%Y-%m-%d")
        ok, msg = seed.mark_attendance(
            self.selected_course_id, student_id, date, status, fid
        )
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=2500)
        self.error = msg
        return rx.toast(msg, duration=2500)

    @rx.event
    async def bulk_attendance(self, status: str):
        fid = await self._faculty_id()
        date = self.attendance_date or datetime.utcnow().strftime("%Y-%m-%d")
        student_ids = [
            e["student_id"]
            for e in seed.ENROLLMENTS
            if e["course_id"] == self.selected_course_id
            and e["status"] == "active"
        ]
        for sid in student_ids:
            seed.mark_attendance(
                self.selected_course_id, sid, date, status, fid
            )
        self.status = f"Marked all students as {status}."
        self.error = ""
        return rx.toast(self.status, duration=3000)

    @rx.event
    async def submit_assessment(self, form_data: dict):
        fid = await self._faculty_id()
        try:
            student_id = int(form_data.get("student_id") or 0)
            course_id = int(form_data.get("course_id") or 0)
            marks = float(form_data.get("marks") or 0)
            max_marks = float(form_data.get("max_marks") or 0)
        except Exception:
            logging.exception("Unexpected error")
            self.error = "Marks and max marks must be numeric."
            self.status = ""
            return rx.toast(self.error, duration=3500)
        title = (form_data.get("title") or "").strip()
        remarks = (form_data.get("remarks") or "").strip()
        if student_id == 0 or course_id == 0 or not title:
            self.error = "Student, course, and title are required."
            self.status = ""
            return rx.toast(self.error, duration=3500)
        ok, msg = seed.add_assessment(
            course_id, student_id, title, marks, max_marks, remarks, fid
        )
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=3000)
        self.error = msg
        self.status = ""
        return rx.toast(msg, duration=3500)

    @rx.event
    async def submit_practical(self, form_data: dict):
        fid = await self._faculty_id()
        try:
            student_id = int(form_data.get("student_id") or 0)
            course_id = int(form_data.get("course_id") or 0)
        except Exception:
            logging.exception("Unexpected error")
            self.error = "Invalid student or course."
            return rx.toast(self.error, duration=3500)
        title = (form_data.get("title") or "").strip()
        grade = (form_data.get("grade") or "").strip()
        remarks = (form_data.get("remarks") or "").strip()
        if student_id == 0 or course_id == 0 or not title or not grade:
            self.error = "Student, course, title, and grade are required."
            self.status = ""
            return rx.toast(self.error, duration=3500)
        ok, msg = seed.add_practical(
            course_id, student_id, title, grade, remarks, fid
        )
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=3000)
        self.error = msg
        return rx.toast(msg, duration=3500)

    @rx.var
    def all_students_list(self) -> list[dict[str, str]]:
        return [
            {"id": str(u["id"]), "name": u["full_name"]}
            for u in seed.all_students()
        ]
