import reflex as rx
from app.components.portal_shell import (
    portal_shell,
    stat_card,
    card,
    empty_state,
    feedback_banner,
)
from app.states.student_state import (
    StudentState,
    CourseView,
    ExamView,
    ResultView,
    DocumentView,
    NotificationView,
    CertificateView,
    AdmitExamView,
)
from app.states.auth_state import AuthState

STUDENT_LINKS: list[tuple[str, str, str]] = [
    ("Dashboard", "#dashboard", "layout-dashboard"),
    ("My Courses", "#courses", "book"),
    ("Exams", "#exams", "file-text"),
    ("Results", "#results", "award"),
    ("Documents", "#documents", "folder"),
    ("Admit Card", "#admit", "id-card"),
    ("Certificates", "#certificates", "scroll"),
    ("Notifications", "#notifications", "bell"),
    ("Profile", "#profile", "user"),
]


def _status_pill(status: str, color: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=f"px-2 py-1 rounded-full text-xs font-semibold w-fit {color}",
    )


def _course_row(c: CourseView) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(c["title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                c["level"] + " · " + c["duration"],
                class_name="text-[#F5EFE0]/50 text-xs mt-1",
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.el.p(
            f"₹{c['fee']:.0f}",
            class_name="text-[#C9A24B] font-semibold hidden md:block",
        ),
        rx.cond(
            c["enrolled"],
            rx.el.button(
                "Drop Course",
                on_click=lambda: StudentState.drop(c["id"]),
                class_name="px-4 py-2 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-sm font-semibold hover:bg-red-500/20",
            ),
            rx.el.button(
                "Enroll",
                on_click=lambda: StudentState.enroll(c["id"]),
                class_name="px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg text-sm font-semibold hover:bg-[#C9A24B]/90",
            ),
        ),
        class_name="flex items-center gap-4 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _exam_row(e: ExamView) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(e["title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                e["course_title"],
                class_name="text-[#F5EFE0]/50 text-xs mt-1",
            ),
            rx.el.div(
                rx.el.span(
                    f"📅 {e['exam_date']}",
                    class_name="text-[#F5EFE0]/60 text-xs",
                ),
                rx.el.span(
                    f"⏰ Apply by {e['application_deadline']}",
                    class_name="text-[#F5EFE0]/60 text-xs",
                ),
                rx.el.span(e["mode"], class_name="text-[#C9A24B] text-xs"),
                class_name="flex flex-wrap gap-3 mt-2",
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.cond(
            e["already_applied"],
            _status_pill(
                "Applied · " + e["application_status"],
                "bg-blue-500/10 text-blue-400 border border-blue-500/30",
            ),
            rx.cond(
                e["past_deadline"],
                _status_pill(
                    "Deadline Passed",
                    "bg-red-500/10 text-red-400 border border-red-500/30",
                ),
                rx.cond(
                    e["enrolled_in_course"],
                    rx.el.button(
                        "Apply Now",
                        on_click=lambda: StudentState.apply_exam(e["id"]),
                        class_name="px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg text-sm font-semibold hover:bg-[#C9A24B]/90",
                    ),
                    _status_pill(
                        "Enroll in course first",
                        "bg-yellow-500/10 text-yellow-400 border border-yellow-500/30",
                    ),
                ),
            ),
        ),
        class_name="flex items-center gap-4 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _result_row(r: ResultView) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(r["exam_title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                r["declared_at"], class_name="text-[#F5EFE0]/40 text-xs mt-1"
            ),
        ),
        rx.el.div(
            rx.el.p(
                f"{r['marks']:.0f} / {r['max_marks']}",
                class_name="text-[#F5EFE0] font-bold text-lg",
            ),
            rx.el.p(
                r["grade"],
                class_name="text-[#C9A24B] text-sm font-semibold",
            ),
            class_name="text-right",
        ),
        class_name="flex items-center justify-between p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _doc_row(d: DocumentView) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(d["doc_type"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(d["file_name"], class_name="text-[#F5EFE0]/50 text-xs"),
            rx.el.p(d["uploaded_at"], class_name="text-[#F5EFE0]/40 text-xs"),
            rx.cond(
                d["reviewer_note"] != "",
                rx.el.p(
                    d["reviewer_note"],
                    class_name="text-[#F5EFE0]/60 text-xs italic mt-1",
                ),
                rx.fragment(),
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.match(
            d["status"],
            (
                "verified",
                _status_pill(
                    "Verified",
                    "bg-green-500/10 text-green-400 border border-green-500/30",
                ),
            ),
            (
                "rejected",
                _status_pill(
                    "Rejected",
                    "bg-red-500/10 text-red-400 border border-red-500/30",
                ),
            ),
            _status_pill(
                "Pending",
                "bg-yellow-500/10 text-yellow-400 border border-yellow-500/30",
            ),
        ),
        class_name="flex items-center gap-4 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _notif_row(n: NotificationView) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(n["title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(n["body"], class_name="text-[#F5EFE0]/60 text-sm mt-1"),
            rx.el.p(
                n["created_at"], class_name="text-[#F5EFE0]/40 text-xs mt-2"
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.cond(
            n["is_read"],
            _status_pill(
                "Read",
                "bg-[#F5EFE0]/5 text-[#F5EFE0]/50 border border-[#F5EFE0]/10",
            ),
            rx.el.button(
                "Mark read",
                on_click=lambda: StudentState.mark_read(n["id"]),
                class_name="px-3 py-1.5 bg-[#C9A24B]/10 border border-[#C9A24B]/30 text-[#C9A24B] rounded-lg text-xs font-semibold hover:bg-[#C9A24B]/20",
            ),
        ),
        class_name="flex items-start gap-4 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _cert_row(c: CertificateView) -> rx.Component:
    return rx.el.div(
        rx.icon("scroll", class_name="h-5 w-5 text-[#C9A24B]"),
        rx.el.div(
            rx.el.p(c["title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                f"Issued {c['issued_at']}",
                class_name="text-[#F5EFE0]/50 text-xs",
            ),
        ),
        rx.match(
            c["status"],
            (
                "issued",
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4"),
                    "Download PDF",
                    on_click=lambda: StudentState.download_certificate(c["id"]),
                    class_name="ml-auto flex items-center gap-2 px-3 py-1.5 bg-[#C9A24B] text-[#0A1628] rounded-lg text-xs font-semibold hover:bg-[#C9A24B]/90",
                ),
            ),
            (
                "rejected",
                _status_pill(
                    "Rejected",
                    "bg-red-500/10 text-red-400 border border-red-500/30 ml-auto",
                ),
            ),
            _status_pill(
                "Pending approval",
                "bg-yellow-500/10 text-yellow-400 border border-yellow-500/30 ml-auto",
            ),
        ),
        class_name="flex items-center gap-3 p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _admit_row(a: AdmitExamView) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(a["exam_title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                f"Exam date: {a['exam_date']}",
                class_name="text-[#F5EFE0]/50 text-xs",
            ),
            class_name="mb-3",
        ),
        rx.cond(
            a["eligible"],
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "circle-check", class_name="h-4 w-4 text-green-400"
                    ),
                    rx.el.span(
                        "You are eligible for the admit card.",
                        class_name="text-green-400 text-sm font-semibold",
                    ),
                    class_name="flex items-center gap-2 p-3 rounded-lg bg-green-500/10 border border-green-500/30 mb-2",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4"),
                    "Download Admit Card PDF",
                    on_click=lambda: StudentState.download_admit_card(
                        a["exam_id"]
                    ),
                    class_name="flex items-center gap-2 px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg text-sm font-semibold hover:bg-[#C9A24B]/90",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "triangle-alert", class_name="h-4 w-4 text-yellow-400"
                    ),
                    rx.el.span(
                        "Requirements not met:",
                        class_name="text-yellow-400 text-sm font-semibold",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                rx.el.ul(
                    rx.foreach(
                        a["reasons"],
                        lambda r: rx.el.li(
                            "• " + r,
                            class_name="text-[#F5EFE0]/70 text-sm py-0.5",
                        ),
                    ),
                    class_name="pl-2",
                ),
                class_name="p-3 rounded-lg bg-yellow-500/5 border border-yellow-500/20",
            ),
        ),
        class_name="p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _section(anchor: str, title: str, *content) -> rx.Component:
    return rx.el.section(
        rx.el.div(id=anchor),
        rx.el.h2(title, class_name="text-2xl font-bold text-[#F5EFE0] mb-4"),
        *content,
        class_name="mb-10 scroll-mt-20",
    )


def student_dashboard() -> rx.Component:
    return portal_shell(
        "Student Portal",
        "Welcome back, " + AuthState.user_name,
        STUDENT_LINKS,
        feedback_banner(StudentState.status, StudentState.error),
        _section(
            "dashboard",
            "Overview",
            rx.el.div(
                stat_card(
                    "Active Courses",
                    StudentState.dashboard_metrics["enrolled"].to_string(),
                    "book",
                ),
                stat_card(
                    "Exam Applications",
                    StudentState.dashboard_metrics["exam_apps"].to_string(),
                    "file-text",
                ),
                stat_card(
                    "Results",
                    StudentState.dashboard_metrics["results"].to_string(),
                    "award",
                ),
                stat_card(
                    "Documents",
                    StudentState.dashboard_metrics["documents"].to_string(),
                    "folder",
                ),
                stat_card(
                    "Certificates",
                    StudentState.dashboard_metrics["certificates"].to_string(),
                    "scroll",
                ),
                stat_card(
                    "Unread Alerts",
                    StudentState.dashboard_metrics["unread_notifs"].to_string(),
                    "bell",
                ),
                class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
            ),
        ),
        _section(
            "courses",
            "My Courses",
            card(
                rx.cond(
                    StudentState.courses.length() > 0,
                    rx.el.div(
                        rx.foreach(StudentState.courses, _course_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "book", "No courses yet", "Enroll in a course to begin."
                    ),
                ),
            ),
        ),
        _section(
            "exams",
            "Exam Applications",
            card(
                rx.cond(
                    StudentState.exams.length() > 0,
                    rx.el.div(
                        rx.foreach(StudentState.exams, _exam_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "file-text", "No exams scheduled", "Check back later."
                    ),
                ),
            ),
        ),
        _section(
            "results",
            "Results",
            card(
                rx.cond(
                    StudentState.results.length() > 0,
                    rx.el.div(
                        rx.foreach(StudentState.results, _result_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "award",
                        "No results yet",
                        "Results appear here once declared.",
                    ),
                ),
            ),
        ),
        _section(
            "documents",
            "Documents",
            card(
                rx.el.div(
                    rx.el.p(
                        "Upload requirements",
                        class_name="text-[#C9A24B] text-xs uppercase tracking-widest font-semibold mb-2",
                    ),
                    rx.el.ul(
                        rx.el.li(
                            "• Allowed file types: PDF, JPG, JPEG, PNG",
                            class_name="text-[#F5EFE0]/60 text-sm",
                        ),
                        rx.el.li(
                            "• Maximum file size: 5 MB",
                            class_name="text-[#F5EFE0]/60 text-sm",
                        ),
                        rx.el.li(
                            "• Clear scans; all details must be legible",
                            class_name="text-[#F5EFE0]/60 text-sm",
                        ),
                        rx.el.li(
                            "• Government ID must be verified before admit card",
                            class_name="text-[#F5EFE0]/60 text-sm",
                        ),
                    ),
                    class_name="p-4 mb-4 rounded-lg bg-[#C9A24B]/5 border border-[#C9A24B]/20",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("ID Proof", value="ID Proof"),
                            rx.el.option("Photo", value="Photo"),
                            rx.el.option(
                                "Address Proof", value="Address Proof"
                            ),
                            rx.el.option(
                                "Educational Certificate",
                                value="Educational Certificate",
                            ),
                            name="doc_type",
                            default_value="ID Proof",
                            class_name="w-full md:w-auto px-4 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                        ),
                        rx.el.input(
                            name="file_name",
                            placeholder="e.g. aadhaar.pdf",
                            class_name="flex-1 px-4 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30",
                        ),
                        rx.el.button(
                            "Upload",
                            type="submit",
                            class_name="px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold text-sm hover:bg-[#C9A24B]/90",
                        ),
                        class_name="flex flex-col md:flex-row gap-2 mb-4",
                    ),
                    on_submit=StudentState.upload_doc,
                    reset_on_submit=True,
                ),
                rx.cond(
                    StudentState.documents.length() > 0,
                    rx.el.div(
                        rx.foreach(StudentState.documents, _doc_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "folder",
                        "No documents yet",
                        "Upload your first document.",
                    ),
                ),
            ),
        ),
        _section(
            "admit",
            "Admit Card Eligibility",
            card(
                rx.cond(
                    StudentState.admit_exams.length() > 0,
                    rx.el.div(
                        rx.foreach(StudentState.admit_exams, _admit_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "id-card",
                        "No exam applications",
                        "Apply for an exam to see admit card status.",
                    ),
                ),
            ),
        ),
        _section(
            "certificates",
            "Certificates",
            card(
                rx.cond(
                    StudentState.certificates.length() > 0,
                    rx.el.div(
                        rx.foreach(StudentState.certificates, _cert_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "scroll",
                        "No certificates yet",
                        "Complete courses to earn certificates.",
                    ),
                ),
            ),
        ),
        _section(
            "notifications",
            "Notifications",
            card(
                rx.cond(
                    StudentState.notifications.length() > 0,
                    rx.el.div(
                        rx.foreach(StudentState.notifications, _notif_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "bell", "No notifications", "You are all caught up."
                    ),
                ),
            ),
        ),
        _section(
            "profile",
            "Profile",
            card(
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Full Name",
                            class_name="block text-[#F5EFE0]/80 text-sm mb-1",
                        ),
                        rx.el.input(
                            name="full_name",
                            default_value=StudentState.profile_full_name,
                            key=StudentState.profile_full_name,
                            class_name="w-full px-4 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Phone",
                            class_name="block text-[#F5EFE0]/80 text-sm mb-1",
                        ),
                        rx.el.input(
                            name="phone",
                            default_value=StudentState.profile_phone,
                            key=StudentState.profile_phone,
                            class_name="w-full px-4 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Address",
                            class_name="block text-[#F5EFE0]/80 text-sm mb-1",
                        ),
                        rx.el.textarea(
                            name="address",
                            default_value=StudentState.profile_address,
                            key=StudentState.profile_address,
                            rows="3",
                            class_name="w-full px-4 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] resize-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.button(
                        "Save Profile",
                        type="submit",
                        class_name="px-6 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90",
                    ),
                    on_submit=StudentState.save_profile,
                ),
            ),
        ),
    )
