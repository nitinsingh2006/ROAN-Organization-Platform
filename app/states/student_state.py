import reflex as rx
from typing import TypedDict
from app.states.auth_state import AuthState
from app.data import seed
import logging


class CourseView(TypedDict):
    id: int
    title: str
    level: str
    duration: str
    fee: float
    enrolled: bool
    enrollment_status: str


class ExamView(TypedDict):
    id: int
    title: str
    course_title: str
    exam_date: str
    application_deadline: str
    mode: str
    venue: str
    already_applied: bool
    past_deadline: bool
    enrolled_in_course: bool
    application_status: str


class ResultView(TypedDict):
    id: int
    exam_title: str
    marks: float
    max_marks: int
    grade: str
    declared_at: str


class DocumentView(TypedDict):
    id: int
    doc_type: str
    file_name: str
    status: str
    uploaded_at: str
    reviewer_note: str


class NotificationView(TypedDict):
    id: int
    title: str
    body: str
    created_at: str
    is_read: bool


class CertificateView(TypedDict):
    id: int
    title: str
    issued_at: str
    status: str


class AdmitExamView(TypedDict):
    exam_id: int
    exam_title: str
    exam_date: str
    eligible: bool
    reasons: list[str]


class StudentState(rx.State):
    status: str = ""
    error: str = ""
    doc_type_input: str = "ID Proof"
    doc_file_name_input: str = ""

    profile_full_name: str = ""
    profile_phone: str = ""
    profile_address: str = ""
    profile_loaded: bool = False

    async def _sid(self) -> int:
        auth = await self.get_state(AuthState)
        return auth.user_id

    @rx.event
    async def load(self):
        auth = await self.get_state(AuthState)
        if auth.user_id == 0:
            return
        prof = seed.student_profile(auth.user_id)
        self.profile_full_name = auth.user_name
        self.profile_phone = prof["phone"] if prof else ""
        self.profile_address = prof["address"] if prof else ""
        self.profile_loaded = True

    @rx.var
    async def courses(self) -> list[CourseView]:
        auth = await self.get_state(AuthState)
        sid = auth.user_id
        enrollments = seed.student_enrollments(sid)
        by_course = {e["course_id"]: e for e in enrollments}
        out: list[CourseView] = []
        for c in seed.COURSES:
            enr = by_course.get(c["id"])
            out.append(
                {
                    "id": c["id"],
                    "title": c["title"],
                    "level": c["level"],
                    "duration": c["duration"],
                    "fee": c["fee"],
                    "enrolled": enr is not None and enr["status"] == "active",
                    "enrollment_status": enr["status"] if enr else "",
                }
            )
        return out

    @rx.var
    async def exams(self) -> list[ExamView]:
        from datetime import datetime

        auth = await self.get_state(AuthState)
        sid = auth.user_id
        active_courses = seed.student_active_course_ids(sid)
        apps = {
            a["exam_id"]: a
            for a in seed.EXAM_APPLICATIONS
            if a["student_id"] == sid
        }
        now = datetime.utcnow()
        out: list[ExamView] = []
        for ex in seed.EXAMS:
            course = seed.find_course(ex["course_id"])
            try:
                deadline = datetime.strptime(
                    ex["application_deadline"], "%Y-%m-%d"
                )
                past = now > deadline
            except Exception:
                logging.exception("Unexpected error")
                past = False
            app = apps.get(ex["id"])
            out.append(
                {
                    "id": ex["id"],
                    "title": ex["title"],
                    "course_title": course["title"] if course else "",
                    "exam_date": ex["exam_date"],
                    "application_deadline": ex["application_deadline"],
                    "mode": ex["mode"],
                    "venue": ex["venue"],
                    "already_applied": app is not None,
                    "past_deadline": past,
                    "enrolled_in_course": ex["course_id"] in active_courses,
                    "application_status": app["status"] if app else "",
                }
            )
        return out

    @rx.var
    async def results(self) -> list[ResultView]:
        auth = await self.get_state(AuthState)
        sid = auth.user_id
        out: list[ResultView] = []
        for r in seed.RESULTS:
            if r["student_id"] == sid and r["declared"]:
                ex = seed.find_exam(r["exam_id"])
                out.append(
                    {
                        "id": r["id"],
                        "exam_title": ex["title"] if ex else "Exam",
                        "marks": r["marks"],
                        "max_marks": r["max_marks"],
                        "grade": r["grade"],
                        "declared_at": r["declared_at"],
                    }
                )
        return out

    @rx.var
    async def documents(self) -> list[DocumentView]:
        auth = await self.get_state(AuthState)
        sid = auth.user_id
        return [
            {
                "id": d["id"],
                "doc_type": d["doc_type"],
                "file_name": d["file_name"],
                "status": d["status"],
                "uploaded_at": d["uploaded_at"],
                "reviewer_note": d["reviewer_note"],
            }
            for d in seed.DOCUMENTS
            if d["student_id"] == sid
        ]

    @rx.var
    async def notifications(self) -> list[NotificationView]:
        auth = await self.get_state(AuthState)
        return [
            {
                "id": n["id"],
                "title": n["title"],
                "body": n["body"],
                "created_at": n["created_at"],
                "is_read": n["is_read"],
            }
            for n in reversed(seed.NOTIFICATIONS)
            if n["user_id"] == auth.user_id
        ]

    @rx.var
    async def certificates(self) -> list[CertificateView]:
        auth = await self.get_state(AuthState)
        return [
            {
                "id": c["id"],
                "title": c["title"],
                "issued_at": c["issued_at"],
                "status": c["status"],
            }
            for c in seed.CERTIFICATES
            if c["student_id"] == auth.user_id
        ]

    @rx.var
    async def admit_exams(self) -> list[AdmitExamView]:
        auth = await self.get_state(AuthState)
        sid = auth.user_id
        out: list[AdmitExamView] = []
        for a in seed.EXAM_APPLICATIONS:
            if a["student_id"] != sid:
                continue
            ex = seed.find_exam(a["exam_id"])
            if ex is None:
                continue
            eligible, reasons = seed.admit_card_eligibility(sid, ex["id"])
            out.append(
                {
                    "exam_id": ex["id"],
                    "exam_title": ex["title"],
                    "exam_date": ex["exam_date"],
                    "eligible": eligible,
                    "reasons": reasons,
                }
            )
        return out

    @rx.var
    async def dashboard_metrics(self) -> dict[str, int]:
        auth = await self.get_state(AuthState)
        sid = auth.user_id
        return {
            "enrolled": len(
                [
                    e
                    for e in seed.ENROLLMENTS
                    if e["student_id"] == sid and e["status"] == "active"
                ]
            ),
            "exam_apps": len(
                [a for a in seed.EXAM_APPLICATIONS if a["student_id"] == sid]
            ),
            "results": len(
                [
                    r
                    for r in seed.RESULTS
                    if r["student_id"] == sid and r["declared"]
                ]
            ),
            "unread_notifs": len(
                [
                    n
                    for n in seed.NOTIFICATIONS
                    if n["user_id"] == sid and not n["is_read"]
                ]
            ),
            "certificates": len(
                [c for c in seed.CERTIFICATES if c["student_id"] == sid]
            ),
            "documents": len(
                [d for d in seed.DOCUMENTS if d["student_id"] == sid]
            ),
        }

    @rx.event
    async def enroll(self, course_id: int):
        sid = await self._sid()
        ok, msg = seed.enroll_student(sid, course_id)
        if ok:
            self.status = msg
            self.error = ""
            seed.push_notification(sid, "Enrollment confirmed", msg)
            return rx.toast(msg, duration=3500)
        self.error = msg
        self.status = ""
        return rx.toast(msg, duration=3500)

    @rx.event
    async def drop(self, course_id: int):
        sid = await self._sid()
        ok, msg = seed.drop_enrollment(sid, course_id)
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=3500)
        self.error = msg
        return rx.toast(msg, duration=3500)

    @rx.event
    async def apply_exam(self, exam_id: int):
        sid = await self._sid()
        ok, msg = seed.apply_for_exam(sid, exam_id)
        if ok:
            self.status = msg
            self.error = ""
            seed.push_notification(sid, "Exam application received", msg)
            return rx.toast(msg, duration=3500)
        self.error = msg
        self.status = ""
        return rx.toast(msg, duration=3500)

    @rx.event
    def set_doc_type(self, v: str):
        self.doc_type_input = v

    @rx.event
    def set_doc_file(self, v: str):
        self.doc_file_name_input = v

    @rx.event
    async def upload_doc(self, form_data: dict):
        sid = await self._sid()
        doc_type = (form_data.get("doc_type") or "").strip()
        file_name = (form_data.get("file_name") or "").strip()
        if not doc_type or not file_name:
            self.error = "Please provide document type and file name."
            self.status = ""
            return rx.toast(self.error, duration=3500)
        ok, msg = seed.upload_document(sid, doc_type, file_name)
        if ok:
            self.status = msg
            self.error = ""
            self.doc_file_name_input = ""
            return rx.toast(msg, duration=3500)
        self.error = msg
        self.status = ""
        return rx.toast(msg, duration=3500)

    @rx.event
    async def mark_read(self, nid: int):
        sid = await self._sid()
        seed.mark_notification_read(nid, sid)

    @rx.event
    def set_profile_name(self, v: str):
        self.profile_full_name = v

    @rx.event
    def set_profile_phone(self, v: str):
        self.profile_phone = v

    @rx.event
    def set_profile_address(self, v: str):
        self.profile_address = v

    @rx.event
    async def download_admit_card(self, exam_id: int):
        sid = await self._sid()
        eligible, reasons = seed.admit_card_eligibility(sid, exam_id)
        if not eligible:
            self.error = "Admit card unavailable: " + "; ".join(reasons)
            return rx.toast(self.error, duration=4500)
        exam = seed.find_exam(exam_id)
        user = seed.find_user_by_id(sid)
        if exam is None or user is None:
            self.error = "Exam not found."
            return rx.toast(self.error, duration=3500)
        from app.utils.pdf_gen import generate_admit_card_pdf

        pdf = generate_admit_card_pdf(
            user["full_name"],
            user["email"],
            exam["title"],
            exam["exam_date"],
            exam["venue"],
            exam["mode"],
            sid,
            exam_id,
        )
        self.status = "Admit card generated."
        self.error = ""
        return rx.download(data=pdf, filename=f"roan_admit_card_{exam_id}.pdf")

    @rx.event
    async def download_certificate(self, cert_id: int):
        sid = await self._sid()
        cert = seed.get_certificate(cert_id)
        if cert is None or cert["student_id"] != sid:
            self.error = "Certificate not found."
            return rx.toast(self.error, duration=3500)
        if cert["status"] != "issued":
            self.error = "Certificate not yet approved by University."
            return rx.toast(self.error, duration=4000)
        user = seed.find_user_by_id(sid)
        from app.utils.pdf_gen import generate_certificate_pdf

        pdf = generate_certificate_pdf(
            user["full_name"] if user else "Student",
            cert["title"],
            cert["issued_at"],
            cert["id"],
        )
        self.status = "Certificate generated."
        self.error = ""
        return rx.download(data=pdf, filename=f"roan_certificate_{cert_id}.pdf")

    @rx.event
    async def save_profile(self, form_data: dict):
        sid = await self._sid()
        name = (form_data.get("full_name") or "").strip()
        phone = (form_data.get("phone") or "").strip()
        address = (form_data.get("address") or "").strip()
        if not name:
            self.error = "Name is required."
            self.status = ""
            return rx.toast(self.error, duration=3500)
        seed.update_profile(sid, name, phone, address)
        self.profile_full_name = name
        self.profile_phone = phone
        self.profile_address = address
        auth = await self.get_state(AuthState)
        auth.user_name = name
        self.status = "Profile updated successfully."
        self.error = ""
        return rx.toast(self.status, duration=3500)
