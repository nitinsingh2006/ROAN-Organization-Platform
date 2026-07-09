import reflex as rx
from app.components.layout import page_shell


def coming_soon_page(
    icon: str, tag: str, title: str, description: str, features: list[str]
) -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(icon, class_name="h-16 w-16 text-[#C9A24B]"),
                        class_name="inline-flex p-6 rounded-3xl bg-[#C9A24B]/10 border border-[#C9A24B]/20 mb-8",
                    ),
                    rx.el.p(
                        f"{tag} · COMING SOON",
                        class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-6",
                    ),
                    rx.el.h1(
                        title,
                        class_name="text-5xl md:text-7xl font-bold text-[#F5EFE0] tracking-tight mb-8",
                    ),
                    rx.el.p(
                        description,
                        class_name="text-lg md:text-xl text-[#F5EFE0]/70 max-w-2xl mx-auto leading-relaxed mb-12",
                    ),
                    rx.el.div(
                        rx.foreach(
                            features,
                            lambda f: rx.el.div(
                                rx.icon(
                                    "check", class_name="h-4 w-4 text-[#C9A24B]"
                                ),
                                rx.el.span(
                                    f, class_name="text-[#F5EFE0]/80 text-sm"
                                ),
                                class_name="flex items-center gap-3 px-5 py-3 bg-[#F5EFE0]/[0.03] rounded-lg border border-[#C9A24B]/10",
                            ),
                        ),
                        class_name="grid sm:grid-cols-2 gap-3 max-w-2xl mx-auto mb-12",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Notify me at launch",
                            rx.icon("bell", class_name="h-4 w-4"),
                            class_name="inline-flex items-center gap-2 px-8 py-4 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
                        ),
                        href="/contact",
                    ),
                    class_name="text-center",
                ),
                class_name="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32",
            ),
        ),
    )


def sufiaana() -> rx.Component:
    return coming_soon_page(
        "chef-hat",
        "SUFIAANA RASOI",
        "Culinary arts, soulfully taught.",
        "A culinary school rooted in the heritage of Sufi and Awadhi kitchens — where every dish is a story of patience, spice, and grace.",
        [
            "Awadhi & Sufi cuisine",
            "Live kitchen studios",
            "Master chef mentorship",
            "Certification programs",
        ],
    )


def infyx() -> rx.Component:
    return coming_soon_page(
        "cpu",
        "INFY-X",
        "Build what tomorrow needs.",
        "Applied technology programs in software engineering, AI, and product development — designed for builders, by builders.",
        [
            "Full-stack engineering",
            "AI & machine learning",
            "Product design tracks",
            "Industry mentorship",
        ],
    )


def xplore() -> rx.Component:
    return coming_soon_page(
        "mountain",
        "XPLORE TRAILS",
        "The mountains are calling.",
        "Guided treks, wilderness camps, and outdoor leadership programs designed to help you discover more of the world — and yourself.",
        [
            "Himalayan expeditions",
            "Wilderness leadership",
            "Certified guides",
            "Small-group cohorts",
        ],
    )
