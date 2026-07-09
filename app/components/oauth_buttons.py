import reflex as rx
from app.states.oauth_state import OAuthState


def oauth_buttons() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="flex-1 h-px bg-[#C9A24B]/20"),
            rx.el.span(
                "OR CONTINUE WITH",
                class_name="px-3 text-[#F5EFE0]/40 text-xs tracking-widest",
            ),
            rx.el.div(class_name="flex-1 h-px bg-[#C9A24B]/20"),
            class_name="flex items-center my-5",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("omega", class_name="h-4 w-4"),
                rx.el.span("Google", class_name="text-sm font-semibold"),
                rx.cond(
                    OAuthState.google_available,
                    rx.fragment(),
                    rx.el.span(
                        "· not configured",
                        class_name="text-[10px] text-[#F5EFE0]/40 ml-1",
                    ),
                ),
                on_click=OAuthState.start_google,
                type="button",
                class_name="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0] rounded-lg hover:bg-[#F5EFE0]/10 hover:border-[#C9A24B]/40 transition-all",
            ),
            rx.el.button(
                rx.icon("git_fork", class_name="h-4 w-4"),
                rx.el.span("GitHub", class_name="text-sm font-semibold"),
                rx.cond(
                    OAuthState.github_available,
                    rx.fragment(),
                    rx.el.span(
                        "· not configured",
                        class_name="text-[10px] text-[#F5EFE0]/40 ml-1",
                    ),
                ),
                on_click=OAuthState.start_github,
                type="button",
                class_name="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 text-[#F5EFE0] rounded-lg hover:bg-[#F5EFE0]/10 hover:border-[#C9A24B]/40 transition-all",
            ),
            class_name="flex flex-col sm:flex-row gap-2",
        ),
        rx.cond(
            OAuthState.error != "",
            rx.el.div(
                rx.icon("triangle-alert", class_name="h-4 w-4 shrink-0"),
                rx.el.span(OAuthState.error, class_name="text-sm"),
                class_name="mt-4 flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg",
            ),
            rx.fragment(),
        ),
    )
