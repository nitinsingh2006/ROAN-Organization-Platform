import reflex as rx
from typing import TypedDict
from app.states.auth_state import AuthState
from app.data import seed
import logging


class ForwardedApp(TypedDict):
    id: int
    student_name: str
    student_email: str
    exam_title: str
    course_title: str
    status: str
    recommended: str
    applied_at: str


class ExamWithApps(TypedDict):
    id: int
    title: str
    course_title: str
    exam_date: str
    max_marks: int
    applications_count: int


class PendingCert(TypedDict):
    id: int
    student_name: str
    title: str
    issued_at: str
    status: str


class AuditRow(TypedDict):
    id: int
    actor_role: str
    action: str
    target_type: str
    target_id: int
    detail: str
    created_at: str


class ApprovedStudentRow(TypedDict):
    student_id: int
    student_name: str
    existing_marks: float
    has_result: bool


class UniversityState(rx.State):
    status: str = ""
    error: str = ""
    selected_exam_id: int = 0
    marks_input: dict[str, str] = {}

    @rx.event
    def set_exam(self, v: str):
        try:
            self.selected_exam_id = int(v)
        except Exception:
            logging.exception("Unexpected error")
            self.selected_exam_id = 0

    @rx.event
    def set_marks(self, sid: str, value: str):
        self.marks_input = {**self.marks_input, sid: value}

    @rx.var
    def metrics(self) -> dict[str, int]:
        return {
            "forwarded": len(
                [
                    a
                    for a in seed.EXAM_APPLICATIONS
                    if a["status"] == "forwarded"
                ]
            ),
            "approved_apps": len(
                [a for a in seed.EXAM_APPLICATIONS if a["status"] == "approved"]
            ),
            "rejected_apps": len(
                [a for a in seed.EXAM_APPLICATIONS if a["status"] == "rejected"]
            ),
            "results_declared": len([r for r in seed.RESULTS if r["declared"]]),
            "pending_certs": len(
                [c for c in seed.CERTIFICATES if c["status"] == "pending"]
            ),
            "issued_certs": len(
                [c for c in seed.CERTIFICATES if c["status"] == "issued"]
            ),
        }

    @rx.var
    def forwarded_queue(self) -> list[ForwardedApp]:
        out: list[ForwardedApp] = []
        for a in seed.EXAM_APPLICATIONS:
            if a["status"] != "forwarded":
                continue
            u = seed.find_user_by_id(a["student_id"])
            ex = seed.find_exam(a["exam_id"])
            course = seed.find_course(ex["course_id"]) if ex else None
            out.append(
                {
                    "id": a["id"],
                    "student_name": u["full_name"] if u else "Unknown",
                    "student_email": u["email"] if u else "",
                    "exam_title": ex["title"] if ex else "",
                    "course_title": course["title"] if course else "",
                    "status": a["status"],
                    "recommended": a["institute_recommended_mode"],
                    "applied_at": a["applied_at"],
                }
            )
        return out

    @rx.var
    def exam_options(self) -> list[dict[str, str]]:
        return [{"id": str(e["id"]), "title": e["title"]} for e in seed.EXAMS]

    @rx.var
    def approved_students_for_exam(self) -> list[ApprovedStudentRow]:
        if self.selected_exam_id == 0:
            return []
        eid = self.selected_exam_id
        out: list[ApprovedStudentRow] = []
        approved_apps = [
            a
            for a in seed.EXAM_APPLICATIONS
            if a["exam_id"] == eid and a["status"] == "approved"
        ]
        for a in approved_apps:
            u = seed.find_user_by_id(a["student_id"])
            if u is None:
                continue
            existing = next(
                (
                    r
                    for r in seed.RESULTS
                    if r["exam_id"] == eid
                    and r["student_id"] == a["student_id"]
                ),
                None,
            )
            out.append(
                {
                    "student_id": a["student_id"],
                    "student_name": u["full_name"],
                    "existing_marks": existing["marks"] if existing else 0.0,
                    "has_result": existing is not None,
                }
            )
        return out

    @rx.var
    def pending_certificates(self) -> list[PendingCert]:
        out: list[PendingCert] = []
        for c in seed.CERTIFICATES:
            if c["status"] not in ("pending", "issued", "rejected"):
                continue
            u = seed.find_user_by_id(c["student_id"])
            out.append(
                {
                    "id": c["id"],
                    "student_name": u["full_name"] if u else "Unknown",
                    "title": c["title"],
                    "issued_at": c["issued_at"],
                    "status": c["status"],
                }
            )
        return out

    @rx.var
    def audit_log(self) -> list[AuditRow]:
        return [
            {
                "id": a["id"],
                "actor_role": a["actor_role"],
                "action": a["action"],
                "target_type": a["target_type"],
                "target_id": a["target_id"],
                "detail": a["detail"],
                "created_at": a["created_at"],
            }
            for a in list(reversed(seed.AUDIT_LOGS))[:50]
            if a["actor_role"] == "university"
        ]

    async def _uid(self) -> int:
        auth = await self.get_state(AuthState)
        return auth.user_id

    @rx.event
    async def approve_app(self, app_id: int):
        uid = await self._uid()
        ok, msg = seed.approve_application(
            app_id, uid, "Approved by University"
        )
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=2500)
        self.error = msg
        return rx.toast(msg, duration=3000)

    @rx.event
    async def reject_app(self, app_id: int):
        uid = await self._uid()
        ok, msg = seed.reject_application(app_id, uid, "Requirements not met")
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=2500)
        self.error = msg
        return rx.toast(msg, duration=3000)

    @rx.event
    async def declare(self, student_id: int):
        self.status = ""
        self.error = ""
        uid = await self._uid()

        # Robust lookup: UI often sends keys as strings, while backend logic uses ints.
        # Check direct lookup, stringified lookup, and exhaustive string-comparison search.
        raw = ""
        str_sid = str(student_id)

        if student_id in self.marks_input:
            raw = self.marks_input[student_id]
        elif str_sid in self.marks_input:
            raw = self.marks_input[str_sid]
        else:
            # Fallback for dynamic TypedDict behavior in compiled JS
            for key, value in self.marks_input.items():
                if str(key) == str_sid:
                    raw = value
                    break

        if not raw:
            self.error = "Please enter a marks value before declaring."
            return rx.toast(self.error, duration=3000)

        try:
            marks = float(raw)
        except ValueError:
            self.error = (
                f"Invalid marks value: '{raw}'. Please enter a valid number."
            )
            return rx.toast(self.error, duration=3000)
        except Exception:
            logging.exception("Unexpected error during marks validation")
            self.error = "An unexpected error occurred while processing marks."
            return rx.toast(self.error, duration=3000)

        ok, msg = seed.declare_result(
            self.selected_exam_id, student_id, marks, uid
        )
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=3000)

        self.error = msg
        self.status = ""
        return rx.toast(msg, duration=3000)

    @rx.event
    async def approve_cert(self, cert_id: int):
        uid = await self._uid()
        ok, msg = seed.approve_certificate(cert_id, uid, "Approved")
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=2500)
        self.error = msg
        return rx.toast(msg, duration=3000)

    @rx.event
    async def reject_cert(self, cert_id: int):
        uid = await self._uid()
        ok, msg = seed.reject_certificate(cert_id, uid, "Not eligible")
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=2500)
        self.error = msg
        return rx.toast(msg, duration=3000)
