import reflex as rx
from app.components.portal_shell import (
    portal_shell,
    stat_card,
    card,
    empty_state,
    feedback_banner,
)
from app.states.institute_state import (
    InstituteState,
    DocumentReview,
    FeeReview,
    AppReview,
)

INSTITUTE_LINKS: list[tuple[str, str, str]] = [
    ("Dashboard", "#dashboard", "layout-dashboard"),
    ("Documents", "#documents", "folder-check"),
    ("Fees", "#fees", "wallet"),
    ("Applications", "#applications", "file-check"),
    ("Forwarded Queue", "#forwarded", "send"),
]


def _doc_row(d: DocumentReview) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                d["student_name"], class_name="text-[#F5EFE0] font-semibold"
            ),
            rx.el.p(d["student_email"], class_name="text-[#F5EFE0]/50 text-xs"),
            rx.el.p(
                d["doc_type"] + " · " + d["file_name"],
                class_name="text-[#C9A24B] text-xs mt-1",
            ),
            rx.el.p(d["uploaded_at"], class_name="text-[#F5EFE0]/40 text-xs"),
        ),
        rx.el.div(
            rx.el.span(
                d["status"],
                class_name="px-2 py-1 rounded-full text-xs font-semibold bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0]/70 mr-2 capitalize",
            ),
            rx.el.button(
                "Verify",
                on_click=lambda: InstituteState.verify_doc(d["id"], "verified"),
                class_name="px-3 py-1.5 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg text-xs font-semibold mr-1",
            ),
            rx.el.button(
                "Reject",
                on_click=lambda: InstituteState.verify_doc(d["id"], "rejected"),
                class_name="px-3 py-1.5 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-xs font-semibold",
            ),
        ),
        class_name="flex items-center justify-between gap-3 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10 flex-wrap",
    )


def _fee_row(f: FeeReview) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                f["student_name"], class_name="text-[#F5EFE0] font-semibold"
            ),
            rx.el.p(f["course_title"], class_name="text-[#F5EFE0]/50 text-xs"),
            rx.el.p(
                f"₹{f['amount']:.0f} · " + f["status"],
                class_name="text-[#C9A24B] text-xs mt-1 capitalize",
            ),
        ),
        rx.el.div(
            rx.el.button(
                "Mark Paid",
                on_click=lambda: InstituteState.update_fee(f["id"], "paid"),
                class_name="px-3 py-1.5 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg text-xs font-semibold mr-1",
            ),
            rx.el.button(
                "Mark Pending",
                on_click=lambda: InstituteState.update_fee(f["id"], "pending"),
                class_name="px-3 py-1.5 bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 rounded-lg text-xs font-semibold mr-1",
            ),
            rx.el.button(
                "Waived",
                on_click=lambda: InstituteState.update_fee(f["id"], "waived"),
                class_name="px-3 py-1.5 bg-blue-500/10 border border-blue-500/30 text-blue-400 rounded-lg text-xs font-semibold",
            ),
        ),
        class_name="flex items-center justify-between gap-3 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10 flex-wrap",
    )


def _app_row(a: AppReview) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                a["student_name"], class_name="text-[#F5EFE0] font-semibold"
            ),
            rx.el.p(a["exam_title"], class_name="text-[#F5EFE0]/50 text-xs"),
            rx.el.p(
                "Status: " + a["status"] + " · Applied " + a["applied_at"],
                class_name="text-[#F5EFE0]/60 text-xs mt-1 capitalize",
            ),
            rx.cond(
                a["recommended"] != "",
                rx.el.p(
                    "Recommended mode: " + a["recommended"],
                    class_name="text-[#C9A24B] text-xs mt-1 font-semibold",
                ),
                rx.fragment(),
            ),
        ),
        rx.el.div(
            rx.el.button(
                "Recommend Online",
                on_click=lambda: InstituteState.recommend_mode(
                    a["id"], "Online"
                ),
                class_name="px-3 py-1.5 bg-blue-500/10 border border-blue-500/30 text-blue-400 rounded-lg text-xs font-semibold mr-1",
            ),
            rx.el.button(
                "Recommend Offline",
                on_click=lambda: InstituteState.recommend_mode(
                    a["id"], "Offline"
                ),
                class_name="px-3 py-1.5 bg-[#C9A24B]/10 border border-[#C9A24B]/30 text-[#C9A24B] rounded-lg text-xs font-semibold",
            ),
        ),
        class_name="flex items-center justify-between gap-3 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10 flex-wrap",
    )


def _fwd_row(a: AppReview) -> rx.Component:
    return rx.el.div(
        rx.icon("send", class_name="h-5 w-5 text-[#C9A24B]"),
        rx.el.div(
            rx.el.p(
                a["student_name"], class_name="text-[#F5EFE0] font-semibold"
            ),
            rx.el.p(a["exam_title"], class_name="text-[#F5EFE0]/50 text-xs"),
            rx.el.p(
                "Forwarded with mode: " + a["recommended"],
                class_name="text-[#C9A24B] text-xs mt-1 font-semibold",
            ),
        ),
        class_name="flex items-start gap-3 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _section(anchor: str, title: str, *content) -> rx.Component:
    return rx.el.section(
        rx.el.div(id=anchor),
        rx.el.h2(title, class_name="text-2xl font-bold text-[#F5EFE0] mb-4"),
        *content,
        class_name="mb-10 scroll-mt-20",
    )


def institute_dashboard() -> rx.Component:
    return portal_shell(
        "Institute Portal",
        "Institute Dashboard",
        INSTITUTE_LINKS,
        feedback_banner(InstituteState.status, InstituteState.error),
        _section(
            "dashboard",
            "Overview",
            rx.el.div(
                stat_card(
                    "Pending Docs",
                    InstituteState.metrics["pending_docs"].to_string(),
                    "folder",
                ),
                stat_card(
                    "Verified Docs",
                    InstituteState.metrics["verified_docs"].to_string(),
                    "shield-check",
                ),
                stat_card(
                    "Pending Fees",
                    InstituteState.metrics["pending_fees"].to_string(),
                    "wallet",
                ),
                stat_card(
                    "Paid Fees",
                    InstituteState.metrics["paid_fees"].to_string(),
                    "circle-dollar-sign",
                ),
                stat_card(
                    "Pending Apps",
                    InstituteState.metrics["pending_apps"].to_string(),
                    "file-text",
                ),
                stat_card(
                    "Forwarded",
                    InstituteState.metrics["forwarded_apps"].to_string(),
                    "send",
                ),
                class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
            ),
        ),
        _section(
            "documents",
            "Document Verification",
            card(
                rx.cond(
                    InstituteState.documents_queue.length() > 0,
                    rx.el.div(
                        rx.foreach(InstituteState.documents_queue, _doc_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "folder", "No documents", "The queue is empty."
                    ),
                ),
            ),
        ),
        _section(
            "fees",
            "Fee Status Management",
            card(
                rx.cond(
                    InstituteState.fees_queue.length() > 0,
                    rx.el.div(
                        rx.foreach(InstituteState.fees_queue, _fee_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "wallet",
                        "No fee records",
                        "Fee records will appear here.",
                    ),
                ),
            ),
        ),
        _section(
            "applications",
            "Exam Applications · Recommend Mode",
            card(
                rx.cond(
                    InstituteState.applications_queue.length() > 0,
                    rx.el.div(
                        rx.foreach(InstituteState.applications_queue, _app_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "file-check",
                        "No applications",
                        "Applications will appear here.",
                    ),
                ),
            ),
        ),
        _section(
            "forwarded",
            "Forwarded to University",
            card(
                rx.cond(
                    InstituteState.forwarded_queue.length() > 0,
                    rx.el.div(
                        rx.foreach(InstituteState.forwarded_queue, _fwd_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "send",
                        "Nothing forwarded",
                        "Recommend a mode to forward applications.",
                    ),
                ),
            ),
        ),
    )
