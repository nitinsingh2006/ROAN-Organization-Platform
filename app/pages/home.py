import reflex as rx
from app.components.layout import page_shell


def _branch_card(
    icon: str, title: str, tag: str, desc: str, href: str, live: bool
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-8 w-8 text-[#C9A24B]"),
                rx.cond(
                    live,
                    rx.el.span(
                        "LIVE",
                        class_name="px-2 py-0.5 bg-[#C9A24B] text-[#0A1628] rounded-full text-[10px] font-bold tracking-wider",
                    ),
                    rx.el.span(
                        "SOON",
                        class_name="px-2 py-0.5 bg-[#F5EFE0]/10 text-[#F5EFE0]/60 rounded-full text-[10px] font-bold tracking-wider",
                    ),
                ),
                class_name="flex items-center justify-between mb-6",
            ),
            rx.el.p(
                tag,
                class_name="text-[#C9A24B] text-xs uppercase tracking-widest font-semibold mb-2",
            ),
            rx.el.h3(
                title, class_name="text-2xl font-bold text-[#F5EFE0] mb-3"
            ),
            rx.el.p(
                desc,
                class_name="text-[#F5EFE0]/60 text-sm leading-relaxed mb-6",
            ),
            rx.el.div(
                rx.el.span(
                    "Explore", class_name="text-[#C9A24B] text-sm font-semibold"
                ),
                rx.icon("arrow-right", class_name="h-4 w-4 text-[#C9A24B]"),
                class_name="flex items-center gap-2 group-hover:gap-3 transition-all",
            ),
            class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] backdrop-blur-xl border border-[#C9A24B]/10 hover:border-[#C9A24B]/40 hover:bg-[#F5EFE0]/[0.06] transition-all duration-300 h-full group",
        ),
        href=href,
    )


def _testimonial(name: str, role: str, text: str) -> rx.Component:
    return rx.el.div(
        rx.icon("quote", class_name="h-6 w-6 text-[#C9A24B] mb-4"),
        rx.el.p(
            text, class_name="text-[#F5EFE0]/80 leading-relaxed mb-6 italic"
        ),
        rx.el.div(
            rx.el.p(name, class_name="text-[#F5EFE0] font-semibold"),
            rx.el.p(
                role,
                class_name="text-[#C9A24B] text-xs uppercase tracking-wider",
            ),
        ),
        class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] backdrop-blur-xl border border-[#C9A24B]/10",
    )


def home() -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "A MULTI-BRANCH LEARNING UNIVERSE",
                        class_name="text-[#C9A24B] text-xs md:text-sm tracking-[0.3em] font-semibold mb-6 animate-fade-in",
                    ),
                    rx.el.h1(
                        "Where craft meets ",
                        rx.el.span(
                            "mastery.", class_name="text-[#C9A24B] italic"
                        ),
                        class_name="text-5xl md:text-7xl lg:text-8xl font-bold text-[#F5EFE0] tracking-tight leading-[1.05] mb-8",
                    ),
                    rx.el.p(
                        "ROAN is home to four passion-led academies — music, culinary arts, technology, and adventure — designed to help you learn deeply, live boldly, and become extraordinary.",
                        class_name="text-lg md:text-xl text-[#F5EFE0]/70 max-w-2xl leading-relaxed mb-10",
                    ),
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                "Explore Guitar Academy",
                                rx.icon("arrow-right", class_name="h-4 w-4"),
                                class_name="flex items-center gap-2 px-8 py-4 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all shadow-2xl shadow-[#C9A24B]/20",
                            ),
                            href="/guitar",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "Learn more",
                                class_name="px-8 py-4 bg-transparent border border-[#F5EFE0]/20 text-[#F5EFE0] rounded-lg font-semibold hover:bg-[#F5EFE0]/5 hover:border-[#C9A24B]/40 transition-all",
                            ),
                            href="/about",
                        ),
                        class_name="flex flex-wrap gap-4",
                    ),
                    class_name="max-w-4xl",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32 relative",
            ),
            class_name="relative overflow-hidden",
        ),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "OUR BRANCHES",
                        class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-3",
                    ),
                    rx.el.h2(
                        "Four worlds, one philosophy.",
                        class_name="text-4xl md:text-5xl font-bold text-[#F5EFE0] mb-4",
                    ),
                    rx.el.p(
                        "Each ROAN branch is a full academy — with its own faculty, curriculum, and community.",
                        class_name="text-[#F5EFE0]/60 max-w-2xl",
                    ),
                    class_name="mb-16",
                ),
                rx.el.div(
                    _branch_card(
                        "guitar",
                        "Guitar Academy",
                        "Music",
                        "Structured programs from beginner acoustic to advanced electric lead, taught by working performing artists.",
                        "/guitar",
                        True,
                    ),
                    _branch_card(
                        "chef-hat",
                        "Sufiaana Rasoi",
                        "Culinary Arts",
                        "A soulful culinary school inspired by heirloom Sufi and Awadhi kitchens — coming soon.",
                        "/sufiaana-rasoi",
                        False,
                    ),
                    _branch_card(
                        "cpu",
                        "Infy-X",
                        "Technology",
                        "Applied programs in software, AI, and product engineering for the next generation of builders.",
                        "/infy-x",
                        False,
                    ),
                    _branch_card(
                        "mountain",
                        "Xplore Trails",
                        "Adventure",
                        "Guided treks, wilderness camps, and outdoor leadership programs across the Himalayas.",
                        "/xplore-trails",
                        False,
                    ),
                    class_name="grid md:grid-cols-2 gap-6",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
            ),
        ),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "TESTIMONIALS",
                        class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-3",
                    ),
                    rx.el.h2(
                        "Voices from our community.",
                        class_name="text-4xl md:text-5xl font-bold text-[#F5EFE0] mb-16",
                    ),
                ),
                rx.el.div(
                    _testimonial(
                        "Aarav Sharma",
                        "Guitar Diploma Student",
                        "ROAN's classical program gave me the technique, the discipline, and the confidence to perform. The faculty genuinely care.",
                    ),
                    _testimonial(
                        "Priya Menon",
                        "Faculty, Guitar Academy",
                        "Teaching at ROAN means being part of a rigorous, artist-first culture. Our students grow into real musicians.",
                    ),
                    _testimonial(
                        "Rahul Verma",
                        "Alumni, Fingerstyle Program",
                        "I walked in playing three chords. I walked out arranging my own instrumentals. The structure here works.",
                    ),
                    class_name="grid md:grid-cols-3 gap-6",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
            ),
        ),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Ready to begin?",
                        class_name="text-4xl md:text-5xl font-bold text-[#F5EFE0] mb-4",
                    ),
                    rx.el.p(
                        "Explore our Guitar Academy — currently accepting new students.",
                        class_name="text-[#F5EFE0]/70 mb-8",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "View Courses",
                            rx.icon("arrow-right", class_name="h-4 w-4"),
                            class_name="inline-flex items-center gap-2 px-8 py-4 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
                        ),
                        href="/guitar",
                    ),
                    class_name="text-center p-12 md:p-20 rounded-3xl bg-gradient-to-br from-[#C9A24B]/10 to-transparent border border-[#C9A24B]/20 backdrop-blur-xl",
                ),
                class_name="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10",
            ),
        ),
    )
