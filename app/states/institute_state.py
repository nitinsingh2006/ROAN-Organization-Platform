import reflex as rx
from typing import TypedDict
from app.states.auth_state import AuthState
from app.data import seed


class DocumentReview(TypedDict):
    id: int
    student_name: str
    student_email: str
    doc_type: str
    file_name: str
    status: str
    uploaded_at: str
    reviewer_note: str


class FeeReview(TypedDict):
    id: int
    student_name: str
    course_title: str
    amount: float
    status: str
    updated_at: str


class AppReview(TypedDict):
    id: int
    student_name: str
    exam_title: str
    status: str
    mode: str
    recommended: str
    applied_at: str


class InstituteState(rx.State):
    status: str = ""
    error: str = ""
    doc_note_input: str = ""

    @rx.var
    def metrics(self) -> dict[str, int]:
        return {
            "pending_docs": len(
                [d for d in seed.DOCUMENTS if d["status"] == "pending"]
            ),
            "verified_docs": len(
                [d for d in seed.DOCUMENTS if d["status"] == "verified"]
            ),
            "pending_fees": len(
                [f for f in seed.FEES if f["status"] == "pending"]
            ),
            "paid_fees": len([f for f in seed.FEES if f["status"] == "paid"]),
            "pending_apps": len(
                [a for a in seed.EXAM_APPLICATIONS if a["status"] == "pending"]
            ),
            "forwarded_apps": len(
                [
                    a
                    for a in seed.EXAM_APPLICATIONS
                    if a["status"] == "forwarded"
                ]
            ),
        }

    @rx.var
    def documents_queue(self) -> list[DocumentReview]:
        out: list[DocumentReview] = []
        for d in seed.DOCUMENTS:
            u = seed.find_user_by_id(d["student_id"])
            out.append(
                {
                    "id": d["id"],
                    "student_name": u["full_name"] if u else "Unknown",
                    "student_email": u["email"] if u else "",
                    "doc_type": d["doc_type"],
                    "file_name": d["file_name"],
                    "status": d["status"],
                    "uploaded_at": d["uploaded_at"],
                    "reviewer_note": d["reviewer_note"],
                }
            )
        return out

    @rx.var
    def fees_queue(self) -> list[FeeReview]:
        out: list[FeeReview] = []
        for f in seed.FEES:
            u = seed.find_user_by_id(f["student_id"])
            c = seed.find_course(f["course_id"])
            out.append(
                {
                    "id": f["id"],
                    "student_name": u["full_name"] if u else "Unknown",
                    "course_title": c["title"] if c else "",
                    "amount": f["amount"],
                    "status": f["status"],
                    "updated_at": f["updated_at"],
                }
            )
        return out

    @rx.var
    def applications_queue(self) -> list[AppReview]:
        out: list[AppReview] = []
        for a in seed.EXAM_APPLICATIONS:
            u = seed.find_user_by_id(a["student_id"])
            ex = seed.find_exam(a["exam_id"])
            out.append(
                {
                    "id": a["id"],
                    "student_name": u["full_name"] if u else "Unknown",
                    "exam_title": ex["title"] if ex else "",
                    "status": a["status"],
                    "mode": a["mode"],
                    "recommended": a["institute_recommended_mode"],
                    "applied_at": a["applied_at"],
                }
            )
        return out

    @rx.var
    def forwarded_queue(self) -> list[AppReview]:
        return [
            a for a in self.applications_queue if a["status"] == "forwarded"
        ]

    async def _uid(self) -> int:
        auth = await self.get_state(AuthState)
        return auth.user_id

    @rx.event
    async def verify_doc(self, doc_id: int, status: str):
        ok, msg = seed.verify_document(doc_id, status, "Reviewed by institute.")
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=2500)
        self.error = msg
        return rx.toast(msg, duration=2500)

    @rx.event
    async def update_fee(self, fee_id: int, status: str):
        uid = await self._uid()
        ok, msg = seed.update_fee_status(fee_id, status, uid)
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=2500)
        self.error = msg
        return rx.toast(msg, duration=2500)

    @rx.event
    async def recommend_mode(self, app_id: int, mode: str):
        ok, msg = seed.recommend_exam_mode(app_id, mode)
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=3000)
        self.error = msg
        return rx.toast(msg, duration=3000)
