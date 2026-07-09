import reflex as rx
from app.states.auth_state import AuthState


class PortalNavState(rx.State):
    sidebar_open: bool = False

    @rx.event
    def toggle(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def close(self):
        self.sidebar_open = False


def _nav_link(
    label: str, href: str, icon: str, active: bool = False
) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label, class_name="text-sm font-medium"),
        href=href,
        on_click=PortalNavState.close,
        class_name="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[#F5EFE0]/70 hover:bg-[#C9A24B]/10 hover:text-[#C9A24B] transition-all",
    )


def _sidebar(
    role_label: str, links: list[tuple[str, str, str]]
) -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("music", class_name="h-6 w-6 text-[#C9A24B]"),
                    rx.el.span(
                        "ROAN",
                        class_name="text-xl font-bold text-[#F5EFE0] tracking-widest",
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="/",
            ),
            rx.el.p(
                role_label,
                class_name="text-[#C9A24B] text-[10px] tracking-[0.3em] font-semibold mt-1",
            ),
            class_name="px-6 py-6 border-b border-[#C9A24B]/10",
        ),
        rx.el.nav(
            rx.foreach(
                links,
                lambda item: _nav_link(item[0], item[1], item[2]),
            ),
            class_name="flex flex-col gap-1 p-4 flex-1 overflow-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.user_email}",
                    class_name="size-10 rounded-full bg-[#F5EFE0]/5",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.user_name,
                        class_name="text-[#F5EFE0] text-sm font-semibold truncate",
                    ),
                    rx.el.p(
                        AuthState.user_email,
                        class_name="text-[#F5EFE0]/50 text-xs truncate",
                    ),
                    class_name="min-w-0 flex-1",
                ),
                class_name="flex items-center gap-3 mb-3",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="h-4 w-4"),
                "Logout",
                on_click=AuthState.logout,
                class_name="w-full flex items-center justify-center gap-2 px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold text-sm hover:bg-[#C9A24B]/90 transition-all",
            ),
            class_name="p-4 border-t border-[#C9A24B]/10",
        ),
        class_name="flex flex-col h-screen w-64 bg-[#0A1628]/95 backdrop-blur-xl border-r border-[#C9A24B]/10 shrink-0",
    )


def _topbar(title: str) -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="h-5 w-5"),
                on_click=PortalNavState.toggle,
                class_name="lg:hidden text-[#F5EFE0] p-2",
            ),
            rx.el.h1(
                title,
                class_name="text-xl md:text-2xl font-bold text-[#F5EFE0]",
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("home", class_name="h-4 w-4"),
                "Public Site",
                href="/",
                class_name="hidden md:flex items-center gap-2 px-3 py-2 text-[#F5EFE0]/60 hover:text-[#C9A24B] text-sm",
            ),
            class_name="flex items-center",
        ),
        class_name="h-16 border-b border-[#C9A24B]/10 bg-[#0A1628]/80 backdrop-blur-xl flex items-center justify-between px-4 md:px-6 sticky top-0 z-30",
    )


def portal_shell(
    role_label: str,
    title: str,
    links: list[tuple[str, str, str]],
    *content,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            _sidebar(role_label, links),
            class_name="hidden lg:block",
        ),
        rx.cond(
            PortalNavState.sidebar_open,
            rx.el.div(
                rx.el.div(
                    on_click=PortalNavState.close,
                    class_name="fixed inset-0 bg-black/60 z-40 lg:hidden",
                ),
                rx.el.div(
                    _sidebar(role_label, links),
                    class_name="fixed left-0 top-0 z-50 lg:hidden animate-fade-in",
                ),
            ),
            rx.fragment(),
        ),
        rx.el.div(
            _topbar(title),
            rx.el.main(
                *content,
                class_name="p-4 md:p-8 max-w-7xl mx-auto",
            ),
            class_name="flex-1 min-w-0 min-h-screen",
        ),
        class_name="flex min-h-screen bg-[#0A1628] font-['Inter'] text-[#F5EFE0]",
    )


def stat_card(
    label: str, value: str, icon: str, accent: str = "text-[#C9A24B]"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-5 w-5 {accent}"),
            rx.el.p(
                label,
                class_name="text-[#F5EFE0]/50 text-xs uppercase tracking-wider font-semibold",
            ),
            class_name="flex items-center gap-2 mb-3",
        ),
        rx.el.p(value, class_name="text-3xl font-bold text-[#F5EFE0]"),
        class_name="p-6 rounded-2xl bg-[#F5EFE0]/[0.03] border border-[#C9A24B]/10 backdrop-blur-xl",
    )


def card(*children, class_name: str = "") -> rx.Component:
    return rx.el.div(
        *children,
        class_name=f"p-6 rounded-2xl bg-[#F5EFE0]/[0.03] border border-[#C9A24B]/10 backdrop-blur-xl {class_name}",
    )


def empty_state(icon: str, title: str, message: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-10 w-10 text-[#C9A24B]/50 mx-auto mb-3"),
        rx.el.p(title, class_name="text-[#F5EFE0] font-semibold mb-1"),
        rx.el.p(message, class_name="text-[#F5EFE0]/50 text-sm"),
        class_name="text-center py-12",
    )


def feedback_banner(status: str, error: str) -> rx.Component:
    return rx.el.div(
        rx.cond(
            error != "",
            rx.el.div(
                rx.icon("triangle-alert", class_name="h-4 w-4 shrink-0"),
                rx.el.span(error, class_name="text-sm"),
                class_name="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg mb-4",
            ),
            rx.fragment(),
        ),
        rx.cond(
            status != "",
            rx.el.div(
                rx.icon("circle-check", class_name="h-4 w-4 shrink-0"),
                rx.el.span(status, class_name="text-sm"),
                class_name="flex items-center gap-2 p-3 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg mb-4",
            ),
            rx.fragment(),
        ),
    )
