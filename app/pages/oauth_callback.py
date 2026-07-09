import reflex as rx
from app.components.layout import page_shell
from app.states.oauth_state import OAuthState


def _loading_view(provider: str) -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.spinner(size="3"),
                    class_name="mb-6 text-[#C9A24B] flex justify-center",
                ),
                rx.el.p(
                    f"COMPLETING {provider.upper()} SIGN-IN",
                    class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-3",
                ),
                rx.el.h1(
                    "Please wait…",
                    class_name="text-3xl md:text-4xl font-bold text-[#F5EFE0] mb-4",
                ),
                rx.el.p(
                    "You will be redirected shortly.",
                    class_name="text-[#F5EFE0]/60",
                ),
                rx.cond(
                    OAuthState.error != "",
                    rx.el.div(
                        OAuthState.error,
                        class_name="mt-6 p-3 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-sm",
                    ),
                    rx.fragment(),
                ),
                class_name="text-center max-w-md mx-auto",
            ),
            class_name="min-h-[70vh] flex items-center justify-center px-4",
        ),
    )


def google_callback() -> rx.Component:
    return _loading_view("google")


def github_callback() -> rx.Component:
    return _loading_view("github")
