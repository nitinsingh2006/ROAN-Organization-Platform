import reflex as rx
from app.components.portal_shell import (
    portal_shell,
    stat_card,
    card,
    empty_state,
    feedback_banner,
)
from app.states.university_state import (
    UniversityState,
    ForwardedApp,
    PendingCert,
    AuditRow,
    ApprovedStudentRow,
)

UNIV_LINKS: list[tuple[str, str, str]] = [
    ("Dashboard", "#dashboard", "layout-dashboard"),
    ("Applications", "#applications", "file-check"),
    ("Declare Results", "#results", "award"),
    ("Certificates", "#certificates", "scroll"),
    ("Audit Trail", "#audit", "history"),
]


def _app_row(a: ForwardedApp) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                a["student_name"], class_name="text-[#F5EFE0] font-semibold"
            ),
            rx.el.p(a["student_email"], class_name="text-[#F5EFE0]/50 text-xs"),
            rx.el.p(
                a["exam_title"] + " · " + a["course_title"],
                class_name="text-[#C9A24B] text-xs mt-1",
            ),
            rx.el.p(
                "Institute recommended: " + a["recommended"],
                class_name="text-[#F5EFE0]/60 text-xs mt-1",
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("check", class_name="h-4 w-4"),
                "Approve",
                on_click=lambda: UniversityState.approve_app(a["id"]),
                class_name="flex items-center gap-1 px-3 py-1.5 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg text-xs font-semibold mr-1",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-4 w-4"),
                "Reject",
                on_click=lambda: UniversityState.reject_app(a["id"]),
                class_name="flex items-center gap-1 px-3 py-1.5 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-xs font-semibold",
            ),
            class_name="flex flex-wrap",
        ),
        class_name="flex items-center justify-between gap-3 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10 flex-wrap",
    )


def _student_result_row(s: ApprovedStudentRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                s["student_name"], class_name="text-[#F5EFE0] font-semibold"
            ),
            rx.cond(
                s["has_result"],
                rx.el.p(
                    f"Current: {s['existing_marks']:.0f}",
                    class_name="text-[#C9A24B] text-xs",
                ),
                rx.el.p(
                    "No result yet",
                    class_name="text-[#F5EFE0]/50 text-xs",
                ),
            ),
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Marks",
                type="number",
                on_change=lambda v: UniversityState.set_marks(
                    s["student_id"].to_string(), v
                ),
                class_name="w-24 px-3 py-1.5 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] text-sm",
            ),
            rx.el.button(
                "Declare",
                on_click=lambda: UniversityState.declare(s["student_id"]),
                class_name="ml-2 px-4 py-1.5 bg-[#C9A24B] text-[#0A1628] rounded-lg text-xs font-semibold hover:bg-[#C9A24B]/90",
            ),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between gap-3 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _cert_row(c: PendingCert) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(c["title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                c["student_name"] + " · " + c["issued_at"],
                class_name="text-[#F5EFE0]/50 text-xs",
            ),
            rx.el.p(
                "Status: " + c["status"],
                class_name="text-[#C9A24B] text-xs mt-1 capitalize",
            ),
        ),
        rx.cond(
            c["status"] == "pending",
            rx.el.div(
                rx.el.button(
                    "Approve",
                    on_click=lambda: UniversityState.approve_cert(c["id"]),
                    class_name="px-3 py-1.5 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg text-xs font-semibold mr-1",
                ),
                rx.el.button(
                    "Reject",
                    on_click=lambda: UniversityState.reject_cert(c["id"]),
                    class_name="px-3 py-1.5 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-xs font-semibold",
                ),
            ),
            rx.el.span(
                c["status"],
                class_name="px-2 py-1 rounded-full text-xs font-semibold bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0]/70 capitalize",
            ),
        ),
        class_name="flex items-center justify-between gap-3 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10 flex-wrap",
    )


def _audit_row(a: AuditRow) -> rx.Component:
    return rx.el.div(
        rx.icon("history", class_name="h-4 w-4 text-[#C9A24B] shrink-0 mt-1"),
        rx.el.div(
            rx.el.p(
                a["action"]
                + " · "
                + a["target_type"]
                + " #"
                + a["target_id"].to_string(),
                class_name="text-[#F5EFE0] font-semibold text-sm",
            ),
            rx.el.p(a["detail"], class_name="text-[#F5EFE0]/60 text-xs"),
            rx.el.p(a["created_at"], class_name="text-[#F5EFE0]/40 text-xs"),
        ),
        class_name="flex items-start gap-3 p-3 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _exam_option(e: dict[str, str]) -> rx.Component:
    return rx.el.option(e["title"], value=e["id"])


def _section(anchor: str, title: str, *content) -> rx.Component:
    return rx.el.section(
        rx.el.div(id=anchor),
        rx.el.h2(title, class_name="text-2xl font-bold text-[#F5EFE0] mb-4"),
        *content,
        class_name="mb-10 scroll-mt-20",
    )


def university_dashboard() -> rx.Component:
    return portal_shell(
        "University Portal",
        "University Dashboard",
        UNIV_LINKS,
        feedback_banner(UniversityState.status, UniversityState.error),
        _section(
            "dashboard",
            "Overview",
            rx.el.div(
                stat_card(
                    "Forwarded",
                    UniversityState.metrics["forwarded"].to_string(),
                    "send",
                ),
                stat_card(
                    "Approved Apps",
                    UniversityState.metrics["approved_apps"].to_string(),
                    "circle-check",
                ),
                stat_card(
                    "Rejected Apps",
                    UniversityState.metrics["rejected_apps"].to_string(),
                    "circle-x",
                ),
                stat_card(
                    "Results Declared",
                    UniversityState.metrics["results_declared"].to_string(),
                    "award",
                ),
                stat_card(
                    "Pending Certs",
                    UniversityState.metrics["pending_certs"].to_string(),
                    "scroll",
                ),
                stat_card(
                    "Issued Certs",
                    UniversityState.metrics["issued_certs"].to_string(),
                    "shield-check",
                ),
                class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
            ),
        ),
        _section(
            "applications",
            "Institute-Forwarded Applications",
            card(
                rx.cond(
                    UniversityState.forwarded_queue.length() > 0,
                    rx.el.div(
                        rx.foreach(UniversityState.forwarded_queue, _app_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "file-check",
                        "Nothing forwarded",
                        "Waiting for institutes to forward applications.",
                    ),
                ),
            ),
        ),
        _section(
            "results",
            "Declare Exam Results",
            card(
                rx.el.div(
                    rx.el.label(
                        "Select Exam",
                        class_name="block text-[#F5EFE0]/70 text-xs mb-1",
                    ),
                    rx.el.select(
                        rx.el.option(
                            "-- select an exam --", value="0", disabled=True
                        ),
                        rx.foreach(UniversityState.exam_options, _exam_option),
                        on_change=UniversityState.set_exam,
                        default_value="0",
                        class_name="w-full px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none mb-4",
                    ),
                ),
                rx.cond(
                    UniversityState.selected_exam_id > 0,
                    rx.cond(
                        UniversityState.approved_students_for_exam.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                UniversityState.approved_students_for_exam,
                                _student_result_row,
                            ),
                            class_name="flex flex-col gap-3",
                        ),
                        empty_state(
                            "users",
                            "No approved students",
                            "Approve applications first.",
                        ),
                    ),
                    rx.el.p(
                        "Select an exam to see approved candidates.",
                        class_name="text-[#F5EFE0]/50 text-sm text-center py-4",
                    ),
                ),
                rx.el.p(
                    "Grading: A+ (≥90%), A (≥80%), B+ (≥70%), B (≥60%), C (≥50%), D (≥40%), F (<40%). Pass mark: 40%.",
                    class_name="text-[#F5EFE0]/50 text-xs mt-4",
                ),
            ),
        ),
        _section(
            "certificates",
            "Certificate Approvals",
            card(
                rx.cond(
                    UniversityState.pending_certificates.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            UniversityState.pending_certificates, _cert_row
                        ),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "scroll",
                        "No certificates",
                        "Declare results to generate certificate candidates.",
                    ),
                ),
            ),
        ),
        _section(
            "audit",
            "Approval Audit Trail",
            card(
                rx.cond(
                    UniversityState.audit_log.length() > 0,
                    rx.el.div(
                        rx.foreach(UniversityState.audit_log, _audit_row),
                        class_name="flex flex-col gap-2",
                    ),
                    empty_state(
                        "history",
                        "No audit entries yet",
                        "Actions you take will appear here.",
                    ),
                ),
            ),
        ),
    )
