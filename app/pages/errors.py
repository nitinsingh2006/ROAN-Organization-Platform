import reflex as rx
from app.components.layout import page_shell


def not_found() -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.el.p(
                    "ERROR 404",
                    class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-4",
                ),
                rx.el.h1(
                    "Lost in the ",
                    rx.el.span(
                        "wilderness.", class_name="text-[#C9A24B] italic"
                    ),
                    class_name="text-6xl md:text-8xl font-bold text-[#F5EFE0] tracking-tight mb-6",
                ),
                rx.el.p(
                    "The page you're looking for doesn't exist — but plenty more does.",
                    class_name="text-lg text-[#F5EFE0]/70 mb-10",
                ),
                rx.el.a(
                    rx.el.button(
                        rx.icon("arrow-left", class_name="h-4 w-4"),
                        "Return home",
                        class_name="inline-flex items-center gap-2 px-8 py-4 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
                    ),
                    href="/",
                ),
                class_name="text-center max-w-2xl mx-auto",
            ),
            class_name="min-h-[70vh] flex items-center justify-center px-4 py-20",
        ),
    )


def not_authorized() -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.icon(
                    "shield-alert",
                    class_name="h-16 w-16 text-[#C9A24B] mx-auto mb-6",
                ),
                rx.el.p(
                    "ACCESS DENIED",
                    class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-4",
                ),
                rx.el.h1(
                    "Not authorized.",
                    class_name="text-5xl md:text-6xl font-bold text-[#F5EFE0] mb-6",
                ),
                rx.el.p(
                    "Your account doesn't have permission to view that page.",
                    class_name="text-lg text-[#F5EFE0]/70 mb-10",
                ),
                rx.el.a(
                    rx.el.button(
                        "Return home",
                        class_name="px-8 py-4 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
                    ),
                    href="/",
                ),
                class_name="text-center max-w-2xl mx-auto",
            ),
            class_name="min-h-[70vh] flex items-center justify-center px-4 py-20",
        ),
    )
