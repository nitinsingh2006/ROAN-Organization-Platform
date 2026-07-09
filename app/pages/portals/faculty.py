import reflex as rx
from app.components.portal_shell import (
    portal_shell,
    stat_card,
    card,
    empty_state,
    feedback_banner,
)
from app.states.faculty_state import (
    FacultyState,
    StudentDirEntry,
    AttendanceRow,
    AssessmentEntry,
    PracticalEntry,
)

FACULTY_LINKS: list[tuple[str, str, str]] = [
    ("Dashboard", "#dashboard", "layout-dashboard"),
    ("Attendance", "#attendance", "check-square"),
    ("Assessments", "#assessments", "clipboard-list"),
    ("Practicals", "#practicals", "wrench"),
    ("Directory", "#directory", "users"),
    ("Reports", "#reports", "bar-chart-3"),
]


def _attendance_row(r: AttendanceRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                r["student_name"], class_name="text-[#F5EFE0] font-semibold"
            ),
            rx.el.p(
                "Current: " + r["status"],
                class_name="text-[#F5EFE0]/50 text-xs",
            ),
        ),
        rx.el.div(
            rx.el.button(
                "Present",
                on_click=lambda: FacultyState.mark_attendance(
                    r["student_id"], "present"
                ),
                class_name=rx.cond(
                    r["status"] == "present",
                    "px-3 py-1.5 bg-green-500/30 border border-green-500/50 text-green-300 rounded-lg text-xs font-semibold",
                    "px-3 py-1.5 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0] rounded-lg text-xs font-semibold hover:bg-green-500/10",
                ),
            ),
            rx.el.button(
                "Absent",
                on_click=lambda: FacultyState.mark_attendance(
                    r["student_id"], "absent"
                ),
                class_name=rx.cond(
                    r["status"] == "absent",
                    "px-3 py-1.5 bg-red-500/30 border border-red-500/50 text-red-300 rounded-lg text-xs font-semibold",
                    "px-3 py-1.5 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0] rounded-lg text-xs font-semibold hover:bg-red-500/10",
                ),
            ),
            rx.el.button(
                "Late",
                on_click=lambda: FacultyState.mark_attendance(
                    r["student_id"], "late"
                ),
                class_name=rx.cond(
                    r["status"] == "late",
                    "px-3 py-1.5 bg-yellow-500/30 border border-yellow-500/50 text-yellow-300 rounded-lg text-xs font-semibold",
                    "px-3 py-1.5 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0] rounded-lg text-xs font-semibold hover:bg-yellow-500/10",
                ),
            ),
            class_name="flex gap-2",
        ),
        class_name="flex items-center justify-between gap-3 p-3 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _directory_row(d: StudentDirEntry) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={d['email']}",
            class_name="size-10 rounded-full",
        ),
        rx.el.div(
            rx.el.p(d["full_name"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(d["email"], class_name="text-[#F5EFE0]/50 text-xs"),
            rx.el.p(
                d["enrolled_courses"], class_name="text-[#C9A24B] text-xs mt-1"
            ),
        ),
        class_name="flex items-center gap-3 p-3 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _assessment_row(a: AssessmentEntry) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(a["title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                a["student_name"] + " · " + a["course_title"],
                class_name="text-[#F5EFE0]/50 text-xs",
            ),
            rx.cond(
                a["remarks"] != "",
                rx.el.p(
                    a["remarks"],
                    class_name="text-[#F5EFE0]/60 text-xs italic mt-1",
                ),
                rx.fragment(),
            ),
        ),
        rx.el.p(
            f"{a['marks']:.0f} / {a['max_marks']:.0f}",
            class_name="text-[#C9A24B] font-bold",
        ),
        class_name="flex items-center justify-between p-3 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _practical_row(p: PracticalEntry) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(p["title"], class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                p["student_name"] + " · " + p["course_title"],
                class_name="text-[#F5EFE0]/50 text-xs",
            ),
            rx.cond(
                p["remarks"] != "",
                rx.el.p(
                    p["remarks"],
                    class_name="text-[#F5EFE0]/60 text-xs italic mt-1",
                ),
                rx.fragment(),
            ),
        ),
        rx.el.p(
            "Grade: " + p["grade"],
            class_name="text-[#C9A24B] font-bold",
        ),
        class_name="flex items-center justify-between p-3 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _course_option(c: dict[str, str]) -> rx.Component:
    return rx.el.option(c["title"], value=c["id"])


def _student_option(s: dict[str, str]) -> rx.Component:
    return rx.el.option(s["name"], value=s["id"])


def _section(anchor: str, title: str, *content) -> rx.Component:
    return rx.el.section(
        rx.el.div(id=anchor),
        rx.el.h2(title, class_name="text-2xl font-bold text-[#F5EFE0] mb-4"),
        *content,
        class_name="mb-10 scroll-mt-20",
    )


def faculty_dashboard() -> rx.Component:
    return portal_shell(
        "Faculty Portal",
        "Faculty Dashboard",
        FACULTY_LINKS,
        rx.el.div(on_mount=FacultyState.init_defaults),
        feedback_banner(FacultyState.status, FacultyState.error),
        _section(
            "dashboard",
            "Overview",
            rx.el.div(
                stat_card(
                    "Students",
                    FacultyState.dashboard_metrics["students"].to_string(),
                    "users",
                ),
                stat_card(
                    "Courses",
                    FacultyState.dashboard_metrics["courses"].to_string(),
                    "book",
                ),
                stat_card(
                    "Attendance Records",
                    FacultyState.dashboard_metrics[
                        "attendance_records"
                    ].to_string(),
                    "check-square",
                ),
                stat_card(
                    "Assessments",
                    FacultyState.dashboard_metrics["assessments"].to_string(),
                    "clipboard-list",
                ),
                stat_card(
                    "Practicals",
                    FacultyState.dashboard_metrics["practicals"].to_string(),
                    "wrench",
                ),
                class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
            ),
        ),
        _section(
            "attendance",
            "Mark Attendance",
            card(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Course",
                            class_name="block text-[#F5EFE0]/70 text-xs mb-1",
                        ),
                        rx.el.select(
                            rx.foreach(
                                FacultyState.course_options, _course_option
                            ),
                            on_change=FacultyState.set_course,
                            value=FacultyState.selected_course_id.to_string(),
                            class_name="w-full px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Date",
                            class_name="block text-[#F5EFE0]/70 text-xs mb-1",
                        ),
                        rx.el.input(
                            type="date",
                            default_value=FacultyState.attendance_date,
                            on_change=FacultyState.set_date.debounce(300),
                            class_name="w-full px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                        ),
                    ),
                    class_name="grid md:grid-cols-2 gap-3 mb-4",
                ),
                rx.el.div(
                    rx.el.button(
                        "Mark all Present",
                        on_click=lambda: FacultyState.bulk_attendance(
                            "present"
                        ),
                        class_name="px-3 py-1.5 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg text-xs font-semibold",
                    ),
                    rx.el.button(
                        "Mark all Absent",
                        on_click=lambda: FacultyState.bulk_attendance("absent"),
                        class_name="px-3 py-1.5 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-xs font-semibold",
                    ),
                    class_name="flex gap-2 mb-4",
                ),
                rx.cond(
                    FacultyState.attendance_roster.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            FacultyState.attendance_roster, _attendance_row
                        ),
                        class_name="flex flex-col gap-2",
                    ),
                    empty_state(
                        "check-square",
                        "No enrolled students",
                        "Select a course with enrollments.",
                    ),
                ),
            ),
        ),
        _section(
            "assessments",
            "Assessments",
            card(
                rx.el.form(
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                FacultyState.all_students_list, _student_option
                            ),
                            name="student_id",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                        ),
                        rx.el.select(
                            rx.foreach(
                                FacultyState.course_options, _course_option
                            ),
                            name="course_id",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                        ),
                        rx.el.input(
                            name="title",
                            placeholder="Assessment title",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                        ),
                        rx.el.input(
                            name="marks",
                            type="number",
                            step="0.1",
                            placeholder="Marks",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                        ),
                        rx.el.input(
                            name="max_marks",
                            type="number",
                            step="0.1",
                            placeholder="Max marks",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                        ),
                        rx.el.input(
                            name="remarks",
                            placeholder="Remarks (optional)",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] md:col-span-2",
                        ),
                        class_name="grid md:grid-cols-2 gap-2 mb-3",
                    ),
                    rx.el.p(
                        "Marks must be between 0 and Max Marks. Max marks must be greater than zero.",
                        class_name="text-[#F5EFE0]/50 text-xs mb-3",
                    ),
                    rx.el.button(
                        "Save Assessment",
                        type="submit",
                        class_name="px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold text-sm hover:bg-[#C9A24B]/90",
                    ),
                    on_submit=FacultyState.submit_assessment,
                    reset_on_submit=True,
                ),
                rx.el.div(class_name="h-px bg-[#C9A24B]/10 my-6"),
                rx.el.h3(
                    "Recent Assessments",
                    class_name="text-[#F5EFE0] font-semibold mb-3",
                ),
                rx.cond(
                    FacultyState.recent_assessments.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            FacultyState.recent_assessments, _assessment_row
                        ),
                        class_name="flex flex-col gap-2",
                    ),
                    empty_state(
                        "clipboard-list",
                        "No assessments yet",
                        "Add your first assessment above.",
                    ),
                ),
            ),
        ),
        _section(
            "practicals",
            "Practical Evaluations",
            card(
                rx.el.form(
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                FacultyState.all_students_list, _student_option
                            ),
                            name="student_id",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                        ),
                        rx.el.select(
                            rx.foreach(
                                FacultyState.course_options, _course_option
                            ),
                            name="course_id",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                        ),
                        rx.el.input(
                            name="title",
                            placeholder="Practical title",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                        ),
                        rx.el.select(
                            rx.el.option("A", value="A"),
                            rx.el.option("B", value="B"),
                            rx.el.option("C", value="C"),
                            rx.el.option("D", value="D"),
                            rx.el.option("F", value="F"),
                            name="grade",
                            default_value="A",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                        ),
                        rx.el.textarea(
                            name="remarks",
                            placeholder="Notes / Remarks",
                            rows="2",
                            class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] md:col-span-2 resize-none",
                        ),
                        class_name="grid md:grid-cols-2 gap-2 mb-3",
                    ),
                    rx.el.button(
                        "Save Practical",
                        type="submit",
                        class_name="px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold text-sm hover:bg-[#C9A24B]/90",
                    ),
                    on_submit=FacultyState.submit_practical,
                    reset_on_submit=True,
                ),
                rx.el.div(class_name="h-px bg-[#C9A24B]/10 my-6"),
                rx.el.h3(
                    "Recent Practicals",
                    class_name="text-[#F5EFE0] font-semibold mb-3",
                ),
                rx.cond(
                    FacultyState.recent_practicals.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            FacultyState.recent_practicals, _practical_row
                        ),
                        class_name="flex flex-col gap-2",
                    ),
                    empty_state(
                        "wrench",
                        "No practicals yet",
                        "Add your first practical above.",
                    ),
                ),
            ),
        ),
        _section(
            "directory",
            "Student Directory",
            card(
                rx.el.input(
                    placeholder="Search students by name or email...",
                    default_value=FacultyState.search_query,
                    on_change=FacultyState.set_search.debounce(300),
                    class_name="w-full px-4 py-2 mb-4 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30",
                ),
                rx.cond(
                    FacultyState.directory.length() > 0,
                    rx.el.div(
                        rx.foreach(FacultyState.directory, _directory_row),
                        class_name="grid md:grid-cols-2 gap-3",
                    ),
                    empty_state(
                        "users", "No students match", "Try a different search."
                    ),
                ),
            ),
        ),
        _section(
            "reports",
            "Reports",
            card(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Total Attendance Records",
                            class_name="text-[#F5EFE0]/50 text-xs uppercase tracking-wider",
                        ),
                        rx.el.p(
                            FacultyState.dashboard_metrics[
                                "attendance_records"
                            ].to_string(),
                            class_name="text-3xl font-bold text-[#C9A24B]",
                        ),
                        class_name="p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Assessments Graded",
                            class_name="text-[#F5EFE0]/50 text-xs uppercase tracking-wider",
                        ),
                        rx.el.p(
                            FacultyState.dashboard_metrics[
                                "assessments"
                            ].to_string(),
                            class_name="text-3xl font-bold text-[#C9A24B]",
                        ),
                        class_name="p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Practicals Graded",
                            class_name="text-[#F5EFE0]/50 text-xs uppercase tracking-wider",
                        ),
                        rx.el.p(
                            FacultyState.dashboard_metrics[
                                "practicals"
                            ].to_string(),
                            class_name="text-3xl font-bold text-[#C9A24B]",
                        ),
                        class_name="p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
                    ),
                    class_name="grid md:grid-cols-3 gap-3",
                ),
            ),
        ),
    )
