import reflex as rx
from app.components.layout import page_shell


def about() -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.el.p(
                    "ABOUT ROAN",
                    class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-6",
                ),
                rx.el.h1(
                    "Craft. Discipline. ",
                    rx.el.span("Soul.", class_name="text-[#C9A24B] italic"),
                    class_name="text-5xl md:text-7xl font-bold text-[#F5EFE0] tracking-tight mb-8",
                ),
                rx.el.p(
                    "ROAN began as a single classical guitar studio. Today it is a growing family of academies — each one built around the same idea: that great teachers, deep curriculum, and honest community can turn passion into mastery.",
                    class_name="text-lg md:text-xl text-[#F5EFE0]/70 max-w-3xl leading-relaxed mb-8",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
            ),
        ),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "target", class_name="h-8 w-8 text-[#C9A24B] mb-4"
                        ),
                        rx.el.h3(
                            "Our Mission",
                            class_name="text-2xl font-bold text-[#F5EFE0] mb-3",
                        ),
                        rx.el.p(
                            "To offer serious, joyful education across the disciplines we love — with real faculty, real curriculum, and real outcomes.",
                            class_name="text-[#F5EFE0]/70 leading-relaxed",
                        ),
                        class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] border border-[#C9A24B]/10 backdrop-blur-xl",
                    ),
                    rx.el.div(
                        rx.icon(
                            "eye", class_name="h-8 w-8 text-[#C9A24B] mb-4"
                        ),
                        rx.el.h3(
                            "Our Vision",
                            class_name="text-2xl font-bold text-[#F5EFE0] mb-3",
                        ),
                        rx.el.p(
                            "A multi-branch learning universe where music, cuisine, technology, and adventure sit under one thoughtful roof.",
                            class_name="text-[#F5EFE0]/70 leading-relaxed",
                        ),
                        class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] border border-[#C9A24B]/10 backdrop-blur-xl",
                    ),
                    rx.el.div(
                        rx.icon(
                            "heart", class_name="h-8 w-8 text-[#C9A24B] mb-4"
                        ),
                        rx.el.h3(
                            "Our Values",
                            class_name="text-2xl font-bold text-[#F5EFE0] mb-3",
                        ),
                        rx.el.p(
                            "Rigor without pretension. Kindness without compromise. Depth over hype. Community over commodification.",
                            class_name="text-[#F5EFE0]/70 leading-relaxed",
                        ),
                        class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] border border-[#C9A24B]/10 backdrop-blur-xl",
                    ),
                    class_name="grid md:grid-cols-3 gap-6",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20",
            ),
        ),
    )
