import reflex as rx
from app.components.portal_shell import (
    portal_shell,
    stat_card,
    card,
    empty_state,
    feedback_banner,
)
from app.states.admin_state import (
    AdminState,
    UserRow,
    ContactRow,
    AuditRow,
    ChartPoint,
    PieSlice,
)

ADMIN_LINKS: list[tuple[str, str, str]] = [
    ("Dashboard", "#dashboard", "layout-dashboard"),
    ("Users", "#users", "users"),
    ("Contact Inbox", "#contacts", "inbox"),
    ("Analytics", "#analytics", "bar-chart-3"),
    ("Audit Log", "#audit", "history"),
    ("Backup", "#backup", "download"),
]


def _user_row(u: UserRow) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={u['email']}",
                    class_name="size-8 rounded-full",
                ),
                rx.el.div(
                    rx.el.p(
                        u["full_name"],
                        class_name="text-[#F5EFE0] font-semibold text-sm",
                    ),
                    rx.el.p(
                        u["email"],
                        class_name="text-[#F5EFE0]/50 text-xs",
                    ),
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.span(
                u["role"].replace("_", " "),
                class_name="px-2 py-1 rounded-full text-xs font-semibold bg-[#C9A24B]/10 text-[#C9A24B] capitalize w-fit",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.cond(
                u["is_active"],
                rx.el.span(
                    "Active",
                    class_name="px-2 py-1 rounded-full text-xs font-semibold bg-green-500/10 text-green-400 border border-green-500/30 w-fit",
                ),
                rx.el.span(
                    "Inactive",
                    class_name="px-2 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/30 w-fit",
                ),
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.button(
                rx.cond(u["is_active"], "Deactivate", "Activate"),
                on_click=lambda: AdminState.toggle_active(u["id"]),
                class_name=rx.cond(
                    u["is_active"],
                    "px-3 py-1.5 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-xs font-semibold",
                    "px-3 py-1.5 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg text-xs font-semibold",
                ),
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-b border-[#C9A24B]/10 hover:bg-[#F5EFE0]/[0.02]",
    )


def _contact_row(m: ContactRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    m["name"], class_name="text-[#F5EFE0] font-semibold text-sm"
                ),
                rx.el.p(
                    m["email"] + " · " + m["branch"],
                    class_name="text-[#F5EFE0]/50 text-xs",
                ),
                class_name="flex-1 min-w-0",
            ),
            rx.el.div(
                rx.cond(
                    m["is_responded"],
                    rx.el.span(
                        "Responded",
                        class_name="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-green-500/10 text-green-400 border border-green-500/30",
                    ),
                    rx.cond(
                        m["is_read"],
                        rx.el.span(
                            "Read",
                            class_name="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/30",
                        ),
                        rx.el.span(
                            "New",
                            class_name="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-[#C9A24B]/20 text-[#C9A24B] border border-[#C9A24B]/40",
                        ),
                    ),
                ),
                class_name="flex flex-col items-end gap-1",
            ),
            class_name="flex items-start justify-between gap-3 mb-2",
        ),
        rx.el.p(
            "Subject: " + m["subject"],
            class_name="text-[#C9A24B] text-xs font-semibold mb-1",
        ),
        rx.el.p(m["message"], class_name="text-[#F5EFE0]/70 text-sm mb-3"),
        rx.el.p(m["created_at"], class_name="text-[#F5EFE0]/40 text-xs mb-3"),
        rx.el.div(
            rx.cond(
                m["is_read"],
                rx.el.button(
                    "Mark unread",
                    on_click=lambda: AdminState.mark_contact(m["id"], False),
                    class_name="px-3 py-1 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0]/70 rounded-lg text-xs font-semibold",
                ),
                rx.el.button(
                    "Mark read",
                    on_click=lambda: AdminState.mark_contact(m["id"], True),
                    class_name="px-3 py-1 bg-blue-500/10 border border-blue-500/30 text-blue-400 rounded-lg text-xs font-semibold",
                ),
            ),
            rx.cond(
                m["is_responded"],
                rx.fragment(),
                rx.el.button(
                    "Mark responded",
                    on_click=lambda: AdminState.mark_responded(m["id"]),
                    class_name="px-3 py-1 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg text-xs font-semibold",
                ),
            ),
            class_name="flex gap-2",
        ),
        class_name="p-4 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _audit_row(a: AuditRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                a["actor_role"].replace("_", " "),
                class_name="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-[#C9A24B]/10 text-[#C9A24B] capitalize",
            ),
            rx.el.span(
                a["created_at"],
                class_name="text-[#F5EFE0]/40 text-xs ml-2",
            ),
            class_name="flex items-center gap-2 mb-1",
        ),
        rx.el.p(
            a["action"]
            + " · "
            + a["target_type"]
            + " #"
            + a["target_id"].to_string(),
            class_name="text-[#F5EFE0] font-semibold text-sm",
        ),
        rx.el.p(a["detail"], class_name="text-[#F5EFE0]/60 text-xs"),
        class_name="p-3 rounded-lg bg-[#F5EFE0]/[0.02] border border-[#C9A24B]/10",
    )


def _pie_slice(p: PieSlice) -> rx.Component:
    return rx.recharts.cell(fill=p["fill"])


def _legend_dot(p: PieSlice) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            class_name="w-3 h-3 rounded-sm shrink-0",
            style={"backgroundColor": p["fill"]},
        ),
        rx.el.span(
            p["name"] + " (" + p["value"].to_string() + ")",
            class_name="text-[#F5EFE0]/80 text-xs",
        ),
        class_name="flex items-center gap-2",
    )


def _chart_card(title: str, chart: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-[#F5EFE0] font-semibold mb-4 text-sm"),
        chart,
        class_name="p-6 rounded-2xl bg-[#F5EFE0]/[0.03] border border-[#C9A24B]/10 backdrop-blur-xl",
    )


def _section(anchor: str, title: str, *content) -> rx.Component:
    return rx.el.section(
        rx.el.div(id=anchor),
        rx.el.h2(title, class_name="text-2xl font-bold text-[#F5EFE0] mb-4"),
        *content,
        class_name="mb-10 scroll-mt-20",
    )


def _analytics_charts() -> rx.Component:
    return rx.el.div(
        _chart_card(
            "User Roles Distribution",
            rx.el.div(
                rx.recharts.pie_chart(
                    rx.recharts.graphing_tooltip(),
                    rx.recharts.pie(
                        rx.foreach(AdminState.role_distribution, _pie_slice),
                        data=AdminState.role_distribution,
                        data_key="value",
                        name_key="name",
                        inner_radius=50,
                        outer_radius=90,
                        stroke="#0A1628",
                        stroke_width=2,
                    ),
                    width="100%",
                    height=250,
                ),
                rx.el.div(
                    rx.foreach(AdminState.role_distribution, _legend_dot),
                    class_name="flex flex-wrap gap-3 mt-2",
                ),
            ),
        ),
        _chart_card(
            "Enrollments by Course",
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False, class_name="opacity-20"
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.bar(
                    data_key="value",
                    fill="#C9A24B",
                    radius=[6, 6, 0, 0],
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "10px"},
                    tick_line=False,
                    axis_line=False,
                    interval=0,
                    angle=-20,
                    height=60,
                ),
                rx.recharts.y_axis(
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "11px"},
                    tick_line=False,
                    axis_line=False,
                ),
                data=AdminState.enrollments_by_course,
                width="100%",
                height=280,
                margin={"left": 10, "right": 10, "top": 15, "bottom": 10},
            ),
        ),
        _chart_card(
            "Applications by Status",
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False, class_name="opacity-20"
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.bar(
                    data_key="value", fill="#8B5CF6", radius=[6, 6, 0, 0]
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "11px"},
                    tick_line=False,
                    axis_line=False,
                ),
                rx.recharts.y_axis(
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "11px"},
                    tick_line=False,
                    axis_line=False,
                ),
                data=AdminState.applications_by_status,
                width="100%",
                height=280,
                margin={"left": 10, "right": 10, "top": 15},
            ),
        ),
        _chart_card(
            "Fees Summary",
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False, class_name="opacity-20"
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.bar(
                    data_key="value", fill="#10B981", radius=[6, 6, 0, 0]
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "11px"},
                    tick_line=False,
                    axis_line=False,
                ),
                rx.recharts.y_axis(
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "11px"},
                    tick_line=False,
                    axis_line=False,
                ),
                data=AdminState.fees_summary,
                width="100%",
                height=280,
                margin={"left": 10, "right": 10, "top": 15},
            ),
        ),
        _chart_card(
            "Student Growth",
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False, class_name="opacity-20"
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.line(
                    data_key="value",
                    stroke="#C9A24B",
                    stroke_width=2,
                    type_="natural",
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "11px"},
                    tick_line=False,
                    axis_line=False,
                ),
                rx.recharts.y_axis(
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "11px"},
                    tick_line=False,
                    axis_line=False,
                ),
                data=AdminState.students_growth,
                width="100%",
                height=280,
                margin={"left": 10, "right": 10, "top": 15},
            ),
        ),
        _chart_card(
            "Results Declared Over Time",
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False, class_name="opacity-20"
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.line(
                    data_key="value",
                    stroke="#3B82F6",
                    stroke_width=2,
                    type_="natural",
                ),
                rx.recharts.x_axis(
                    data_key="name",
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "10px"},
                    tick_line=False,
                    axis_line=False,
                ),
                rx.recharts.y_axis(
                    stroke="#F5EFE0",
                    custom_attrs={"fontSize": "11px"},
                    tick_line=False,
                    axis_line=False,
                ),
                data=AdminState.results_over_time,
                width="100%",
                height=280,
                margin={"left": 10, "right": 10, "top": 15},
            ),
        ),
        class_name="grid md:grid-cols-2 gap-4",
    )


def admin_dashboard() -> rx.Component:
    return portal_shell(
        "Super Admin",
        "Super Admin Dashboard",
        ADMIN_LINKS,
        feedback_banner(AdminState.status, AdminState.error),
        _section(
            "dashboard",
            "Platform Overview",
            rx.el.div(
                stat_card(
                    "Total Users",
                    AdminState.metrics["users"].to_string(),
                    "users",
                ),
                stat_card(
                    "Students",
                    AdminState.metrics["students"].to_string(),
                    "graduation-cap",
                ),
                stat_card(
                    "Faculty",
                    AdminState.metrics["faculty"].to_string(),
                    "user-cog",
                ),
                stat_card(
                    "Courses",
                    AdminState.metrics["courses"].to_string(),
                    "book",
                ),
                stat_card(
                    "Enrollments",
                    AdminState.metrics["enrollments"].to_string(),
                    "clipboard",
                ),
                stat_card(
                    "Exam Apps",
                    AdminState.metrics["exam_apps"].to_string(),
                    "file-text",
                ),
                stat_card(
                    "Results",
                    AdminState.metrics["results"].to_string(),
                    "award",
                ),
                stat_card(
                    "Certificates",
                    AdminState.metrics["certificates"].to_string(),
                    "scroll",
                ),
                stat_card(
                    "Unread Messages",
                    AdminState.metrics["unread_contacts"].to_string(),
                    "inbox",
                ),
                stat_card(
                    "Audit Entries",
                    AdminState.metrics["audit_logs"].to_string(),
                    "history",
                ),
                stat_card(
                    "Inactive Users",
                    AdminState.metrics["inactive_users"].to_string(),
                    "user-x",
                ),
                stat_card(
                    "Contact Total",
                    AdminState.metrics["contacts"].to_string(),
                    "mail",
                ),
                class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4",
            ),
        ),
        _section(
            "users",
            "User Management",
            card(
                rx.el.div(
                    rx.el.h3(
                        "Create User",
                        class_name="text-[#F5EFE0] font-semibold mb-3",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.input(
                                name="full_name",
                                placeholder="Full name",
                                class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                            ),
                            rx.el.input(
                                name="email",
                                placeholder="Email",
                                type="email",
                                class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                            ),
                            rx.el.input(
                                name="password",
                                placeholder="Password (min 6 chars)",
                                type="password",
                                class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0]",
                            ),
                            rx.el.select(
                                rx.el.option("Student", value="student"),
                                rx.el.option("Faculty", value="faculty"),
                                rx.el.option("Institute", value="institute"),
                                rx.el.option("University", value="university"),
                                rx.el.option(
                                    "Super Admin", value="super_admin"
                                ),
                                name="role",
                                default_value="student",
                                class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                            ),
                            class_name="grid md:grid-cols-2 gap-2 mb-3",
                        ),
                        rx.el.button(
                            "Create User",
                            type="submit",
                            class_name="px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold text-sm hover:bg-[#C9A24B]/90",
                        ),
                        on_submit=AdminState.create_user,
                        reset_on_submit=True,
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Search name or email...",
                        default_value=AdminState.user_search,
                        on_change=AdminState.set_user_search.debounce(300),
                        class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] flex-1",
                    ),
                    rx.el.select(
                        rx.el.option("All Roles", value="all"),
                        rx.el.option("Student", value="student"),
                        rx.el.option("Faculty", value="faculty"),
                        rx.el.option("Institute", value="institute"),
                        rx.el.option("University", value="university"),
                        rx.el.option("Super Admin", value="super_admin"),
                        on_change=AdminState.set_role_filter,
                        value=AdminState.role_filter,
                        class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                    ),
                    rx.el.select(
                        rx.el.option("All Statuses", value="all"),
                        rx.el.option("Active", value="active"),
                        rx.el.option("Inactive", value="inactive"),
                        on_change=AdminState.set_status_filter,
                        value=AdminState.status_filter,
                        class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none",
                    ),
                    class_name="flex flex-wrap gap-2 mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "User",
                                    class_name="px-4 py-2 text-left text-[#F5EFE0]/50 text-xs uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Role",
                                    class_name="px-4 py-2 text-left text-[#F5EFE0]/50 text-xs uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-4 py-2 text-left text-[#F5EFE0]/50 text-xs uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Action",
                                    class_name="px-4 py-2 text-left text-[#F5EFE0]/50 text-xs uppercase tracking-wider",
                                ),
                            ),
                        ),
                        rx.el.tbody(
                            rx.foreach(AdminState.users_filtered, _user_row),
                        ),
                        class_name="table-auto w-full",
                    ),
                    class_name="overflow-x-auto",
                ),
            ),
        ),
        _section(
            "contacts",
            "Contact Message Inbox",
            card(
                rx.cond(
                    AdminState.contacts_list.length() > 0,
                    rx.el.div(
                        rx.foreach(AdminState.contacts_list, _contact_row),
                        class_name="flex flex-col gap-3",
                    ),
                    empty_state(
                        "inbox",
                        "No messages yet",
                        "Submissions from the public contact form will appear here.",
                    ),
                ),
            ),
        ),
        _section(
            "analytics",
            "Platform Analytics",
            _analytics_charts(),
        ),
        _section(
            "audit",
            "Audit Log",
            card(
                rx.el.div(
                    rx.el.select(
                        rx.el.option("All Roles", value="all"),
                        rx.el.option("Student", value="student"),
                        rx.el.option("Faculty", value="faculty"),
                        rx.el.option("Institute", value="institute"),
                        rx.el.option("University", value="university"),
                        rx.el.option("Super Admin", value="super_admin"),
                        rx.el.option("System", value="system"),
                        on_change=AdminState.set_audit_role,
                        value=AdminState.audit_role_filter,
                        class_name="px-3 py-2 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] appearance-none mb-4",
                    ),
                ),
                rx.cond(
                    AdminState.audit_page_rows.length() > 0,
                    rx.el.div(
                        rx.foreach(AdminState.audit_page_rows, _audit_row),
                        class_name="flex flex-col gap-2",
                    ),
                    empty_state(
                        "history",
                        "No audit entries",
                        "Actions will appear here.",
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("chevron-left", class_name="h-4 w-4"),
                        "Prev",
                        on_click=AdminState.audit_prev,
                        class_name="flex items-center gap-1 px-3 py-1.5 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0] rounded-lg text-xs font-semibold",
                    ),
                    rx.el.span(
                        "Page ",
                        AdminState.audit_page.to_string(),
                        " of ",
                        AdminState.audit_total_pages.to_string(),
                        class_name="text-[#F5EFE0]/60 text-xs",
                    ),
                    rx.el.button(
                        "Next",
                        rx.icon("chevron-right", class_name="h-4 w-4"),
                        on_click=AdminState.audit_next,
                        class_name="flex items-center gap-1 px-3 py-1.5 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0] rounded-lg text-xs font-semibold",
                    ),
                    class_name="flex items-center justify-between mt-4",
                ),
            ),
        ),
        _section(
            "backup",
            "Data Backup",
            card(
                rx.el.p(
                    "Download a full JSON backup of all platform data — users, courses, enrollments, exams, results, documents, notifications, fees, certificates, audit logs, and contact messages.",
                    class_name="text-[#F5EFE0]/70 mb-4 text-sm",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4"),
                    "Download JSON Backup",
                    on_click=AdminState.export_backup,
                    class_name="flex items-center gap-2 px-6 py-3 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90",
                ),
            ),
        ),
    )
