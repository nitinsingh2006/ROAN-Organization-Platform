import reflex as rx
from typing import TypedDict
import json
from app.states.auth_state import AuthState
from app.data import seed
import logging


class UserRow(TypedDict):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool


class ContactRow(TypedDict):
    id: int
    name: str
    email: str
    branch: str
    subject: str
    message: str
    created_at: str
    is_read: bool
    is_responded: bool


class AuditRow(TypedDict):
    id: int
    actor_role: str
    action: str
    target_type: str
    target_id: int
    detail: str
    created_at: str


class ChartPoint(TypedDict):
    name: str
    value: int


class PieSlice(TypedDict):
    name: str
    value: int
    fill: str


class AdminState(rx.State):
    status: str = ""
    error: str = ""
    role_filter: str = "all"
    status_filter: str = "all"
    user_search: str = ""
    audit_role_filter: str = "all"
    audit_page: int = 1
    audit_page_size: int = 10

    @rx.event
    def set_role_filter(self, v: str):
        self.role_filter = v

    @rx.event
    def set_status_filter(self, v: str):
        self.status_filter = v

    @rx.event
    def set_user_search(self, v: str):
        self.user_search = v

    @rx.event
    def set_audit_role(self, v: str):
        self.audit_role_filter = v
        self.audit_page = 1

    @rx.event
    def audit_next(self):
        if self.audit_page < self.audit_total_pages:
            self.audit_page += 1

    @rx.event
    def audit_prev(self):
        if self.audit_page > 1:
            self.audit_page -= 1

    @rx.var
    def metrics(self) -> dict[str, int]:
        return {
            "users": len(seed.USERS),
            "students": len(seed.all_students()),
            "faculty": len([u for u in seed.USERS if u["role"] == "faculty"]),
            "courses": len(seed.COURSES),
            "enrollments": len(
                [e for e in seed.ENROLLMENTS if e["status"] == "active"]
            ),
            "exam_apps": len(seed.EXAM_APPLICATIONS),
            "results": len([r for r in seed.RESULTS if r["declared"]]),
            "certificates": len(
                [c for c in seed.CERTIFICATES if c["status"] == "issued"]
            ),
            "contacts": len(seed.CONTACT_MESSAGES),
            "unread_contacts": len(
                [m for m in seed.CONTACT_MESSAGES if not m["is_read"]]
            ),
            "audit_logs": len(seed.AUDIT_LOGS),
            "inactive_users": len(
                [u for u in seed.USERS if not u["is_active"]]
            ),
        }

    @rx.var
    def users_filtered(self) -> list[UserRow]:
        q = self.user_search.lower().strip()
        rows: list[UserRow] = []
        for u in seed.USERS:
            if self.role_filter != "all" and u["role"] != self.role_filter:
                continue
            if self.status_filter == "active" and not u["is_active"]:
                continue
            if self.status_filter == "inactive" and u["is_active"]:
                continue
            if (
                q
                and q not in u["full_name"].lower()
                and q not in u["email"].lower()
            ):
                continue
            rows.append(
                {
                    "id": u["id"],
                    "email": u["email"],
                    "full_name": u["full_name"],
                    "role": u["role"],
                    "is_active": u["is_active"],
                }
            )
        return rows

    @rx.var
    def contacts_list(self) -> list[ContactRow]:
        return [
            {
                "id": m["id"],
                "name": m["name"],
                "email": m["email"],
                "branch": m["branch"],
                "subject": m["subject"] or "(no subject)",
                "message": m["message"],
                "created_at": m["created_at"],
                "is_read": m["is_read"],
                "is_responded": m["is_responded"],
            }
            for m in reversed(seed.CONTACT_MESSAGES)
        ]

    @rx.var
    def audit_filtered(self) -> list[AuditRow]:
        rows: list[AuditRow] = []
        for a in reversed(seed.AUDIT_LOGS):
            if (
                self.audit_role_filter != "all"
                and a["actor_role"] != self.audit_role_filter
            ):
                continue
            rows.append(
                {
                    "id": a["id"],
                    "actor_role": a["actor_role"],
                    "action": a["action"],
                    "target_type": a["target_type"],
                    "target_id": a["target_id"],
                    "detail": a["detail"],
                    "created_at": a["created_at"],
                }
            )
        return rows

    @rx.var
    def audit_total_pages(self) -> int:
        total = len(self.audit_filtered)
        return max(1, -(-total // self.audit_page_size))

    @rx.var
    def audit_page_rows(self) -> list[AuditRow]:
        start = (self.audit_page - 1) * self.audit_page_size
        end = start + self.audit_page_size
        return self.audit_filtered[start:end]

    @rx.var
    def role_distribution(self) -> list[PieSlice]:
        role_colors = {
            "student": "#C9A24B",
            "faculty": "#8B5CF6",
            "institute": "#3B82F6",
            "university": "#10B981",
            "super_admin": "#EF4444",
        }
        counts: dict[str, int] = {}
        for u in seed.USERS:
            counts[u["role"]] = counts.get(u["role"], 0) + 1
        return [
            {
                "name": role.replace("_", " ").title(),
                "value": counts[role],
                "fill": role_colors.get(role, "#F5EFE0"),
            }
            for role in counts
        ]

    @rx.var
    def enrollments_by_course(self) -> list[ChartPoint]:
        out: list[ChartPoint] = []
        for c in seed.COURSES:
            count = len(
                [
                    e
                    for e in seed.ENROLLMENTS
                    if e["course_id"] == c["id"] and e["status"] == "active"
                ]
            )
            out.append(
                {
                    "name": c["title"][:20]
                    + ("…" if len(c["title"]) > 20 else ""),
                    "value": count,
                }
            )
        return out

    @rx.var
    def applications_by_status(self) -> list[ChartPoint]:
        counts: dict[str, int] = {
            "pending": 0,
            "forwarded": 0,
            "approved": 0,
            "rejected": 0,
        }
        for a in seed.EXAM_APPLICATIONS:
            counts[a["status"]] = counts.get(a["status"], 0) + 1
        return [{"name": k.title(), "value": v} for k, v in counts.items()]

    @rx.var
    def fees_summary(self) -> list[ChartPoint]:
        counts: dict[str, int] = {"paid": 0, "pending": 0, "waived": 0}
        for f in seed.FEES:
            counts[f["status"]] = counts.get(f["status"], 0) + 1
        return [{"name": k.title(), "value": v} for k, v in counts.items()]

    @rx.var
    def results_over_time(self) -> list[ChartPoint]:
        buckets: dict[str, int] = {}
        for r in seed.RESULTS:
            if not r["declared"]:
                continue
            day = r["declared_at"][:10]
            buckets[day] = buckets.get(day, 0) + 1
        items = sorted(buckets.items())
        return [{"name": d, "value": v} for d, v in items]

    @rx.var
    def students_growth(self) -> list[ChartPoint]:
        # Snapshot growth by grouping user ids into buckets
        total = 0
        out: list[ChartPoint] = []
        students = seed.all_students()
        chunk = max(1, len(students) // 6)
        for i in range(0, len(students), chunk):
            total += len(students[i : i + chunk])
            out.append({"name": f"W{len(out) + 1}", "value": total})
        return out

    async def _uid(self) -> int:
        auth = await self.get_state(AuthState)
        return auth.user_id

    @rx.event
    async def create_user(self, form_data: dict):
        uid = await self._uid()
        email = (form_data.get("email") or "").strip()
        password = form_data.get("password") or ""
        full_name = (form_data.get("full_name") or "").strip()
        role = form_data.get("role") or "student"
        ok, msg = seed.admin_create_user(email, password, full_name, role, uid)
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=3000)
        self.error = msg
        self.status = ""
        return rx.toast(msg, duration=3500)

    @rx.event
    async def toggle_active(self, target_id: int):
        uid = await self._uid()
        ok, msg = seed.toggle_user_active(target_id, uid)
        if ok:
            self.status = msg
            self.error = ""
            return rx.toast(msg, duration=2500)
        self.error = msg
        return rx.toast(msg, duration=3000)

    @rx.event
    def mark_contact(self, cid: int, is_read: bool):
        seed.mark_contact_read(cid, is_read)

    @rx.event
    def mark_responded(self, cid: int):
        seed.mark_contact_responded(cid, True)

    @rx.event
    def export_backup(self):
        payload = {
            "users": seed.USERS,
            "courses": seed.COURSES,
            "enrollments": seed.ENROLLMENTS,
            "exams": seed.EXAMS,
            "exam_applications": seed.EXAM_APPLICATIONS,
            "results": seed.RESULTS,
            "documents": seed.DOCUMENTS,
            "notifications": seed.NOTIFICATIONS,
            "fees": seed.FEES,
            "certificates": seed.CERTIFICATES,
            "attendance": seed.ATTENDANCE,
            "assessments": seed.ASSESSMENTS,
            "practicals": seed.PRACTICALS,
            "audit_logs": seed.AUDIT_LOGS,
            "contact_messages": seed.CONTACT_MESSAGES,
            "student_profiles": seed.STUDENT_PROFILES,
        }
        data = json.dumps(payload, indent=2, default=str)
        return rx.download(data=data, filename="roan_backup.json")
