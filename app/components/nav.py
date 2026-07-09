import reflex as rx
from app.states.auth_state import AuthState


class NavState(rx.State):
    mobile_open: bool = False

    @rx.event
    def toggle_mobile(self):
        self.mobile_open = not self.mobile_open

    @rx.event
    def close_mobile(self):
        self.mobile_open = False


def _nav_link(label: str, href: str) -> rx.Component:
    return rx.el.a(
        label,
        href=href,
        class_name="text-[#F5EFE0]/80 hover:text-[#C9A24B] transition-colors duration-200 font-medium text-sm tracking-wide",
    )


def _mobile_link(label: str, href: str) -> rx.Component:
    return rx.el.a(
        label,
        href=href,
        on_click=NavState.close_mobile,
        class_name="block px-4 py-3 text-[#F5EFE0] hover:bg-[#C9A24B]/10 hover:text-[#C9A24B] rounded-lg transition-colors font-medium",
    )


def nav() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("music", class_name="h-6 w-6 text-[#C9A24B]"),
                    rx.el.span(
                        "ROAN",
                        class_name="text-2xl font-bold text-[#F5EFE0] tracking-widest",
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="/",
            ),
            rx.el.div(
                _nav_link("Home", "/"),
                _nav_link("Guitar Academy", "/guitar"),
                _nav_link("Sufiaana Rasoi", "/sufiaana-rasoi"),
                _nav_link("Infy-X", "/infy-x"),
                _nav_link("Xplore Trails", "/xplore-trails"),
                _nav_link("About", "/about"),
                _nav_link("Contact", "/contact"),
                class_name="hidden lg:flex items-center gap-7",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.span(
                            AuthState.user_name,
                            class_name="text-[#F5EFE0]/80 text-sm hidden md:inline",
                        ),
                        rx.el.button(
                            "Logout",
                            on_click=AuthState.logout,
                            class_name="px-4 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all text-sm",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.el.a(
                        rx.el.button(
                            rx.icon("user", class_name="h-4 w-4"),
                            "Student Portal",
                            class_name="hidden md:flex items-center gap-2 px-5 py-2 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all text-sm shadow-lg shadow-[#C9A24B]/20",
                        ),
                        href="/login",
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        NavState.mobile_open,
                        rx.icon("x", class_name="h-6 w-6"),
                        rx.icon("menu", class_name="h-6 w-6"),
                    ),
                    on_click=NavState.toggle_mobile,
                    class_name="lg:hidden text-[#F5EFE0] ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16",
        ),
        rx.cond(
            NavState.mobile_open,
            rx.el.div(
                _mobile_link("Home", "/"),
                _mobile_link("Guitar Academy", "/guitar"),
                _mobile_link("Sufiaana Rasoi", "/sufiaana-rasoi"),
                _mobile_link("Infy-X", "/infy-x"),
                _mobile_link("Xplore Trails", "/xplore-trails"),
                _mobile_link("About", "/about"),
                _mobile_link("Contact", "/contact"),
                _mobile_link("Student Portal", "/login"),
                class_name="lg:hidden px-4 pb-4 space-y-1 bg-[#0A1628]/95 backdrop-blur-lg border-t border-[#C9A24B]/10",
            ),
            rx.fragment(),
        ),
        class_name="sticky top-0 z-50 bg-[#0A1628]/80 backdrop-blur-xl border-b border-[#C9A24B]/10",
    )
