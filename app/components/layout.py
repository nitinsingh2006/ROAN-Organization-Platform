import reflex as rx
from app.components.nav import nav
from app.components.footer import footer


def page_shell(*children) -> rx.Component:
    return rx.el.div(
        nav(),
        rx.el.main(
            *children,
            class_name="min-h-screen animate-fade-in",
        ),
        footer(),
        class_name="bg-[#0A1628] min-h-screen font-['Inter'] text-[#F5EFE0]",
    )
