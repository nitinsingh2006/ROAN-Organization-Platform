import reflex as rx
from app.components.layout import page_shell
from app.states.course_state import CourseState
from app.data.seed import CourseRec


def _course_card(course: CourseRec) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                course["level"],
                class_name="px-3 py-1 bg-[#C9A24B]/10 text-[#C9A24B] rounded-full text-xs font-semibold tracking-wide w-fit",
            ),
            rx.el.span(
                course["duration"], class_name="text-[#F5EFE0]/50 text-xs"
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.h3(
            course["title"], class_name="text-xl font-bold text-[#F5EFE0] mb-3"
        ),
        rx.el.p(
            course["description"],
            class_name="text-[#F5EFE0]/60 text-sm leading-relaxed mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Fee",
                    class_name="text-[#F5EFE0]/40 text-xs uppercase tracking-wider",
                ),
                rx.el.p(
                    f"₹{course['fee']:.0f}",
                    class_name="text-[#C9A24B] text-2xl font-bold",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Seats",
                    class_name="text-[#F5EFE0]/40 text-xs uppercase tracking-wider",
                ),
                rx.el.p(
                    course["seats"].to_string(),
                    class_name="text-[#F5EFE0] text-2xl font-bold",
                ),
                class_name="text-right",
            ),
            class_name="flex items-end justify-between pt-4 border-t border-[#C9A24B]/10",
        ),
        class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] backdrop-blur-xl border border-[#C9A24B]/10 hover:border-[#C9A24B]/40 transition-all duration-300 tilt-card",
    )


def guitar() -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.el.p(
                    "BRANCH · LIVE",
                    class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-6",
                ),
                rx.el.h1(
                    "Guitar ",
                    rx.el.span("Academy.", class_name="text-[#C9A24B] italic"),
                    class_name="text-5xl md:text-7xl font-bold text-[#F5EFE0] tracking-tight mb-6",
                ),
                rx.el.p(
                    "From your first strum to full stage performance — a university-affiliated music school for serious guitarists.",
                    class_name="text-lg md:text-xl text-[#F5EFE0]/70 max-w-2xl leading-relaxed",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
            ),
        ),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "PROGRAMS",
                        class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-3",
                    ),
                    rx.el.h2(
                        "Our Courses",
                        class_name="text-4xl font-bold text-[#F5EFE0] mb-4",
                    ),
                    rx.el.p(
                        "Six structured programs — each taught by working performing artists.",
                        class_name="text-[#F5EFE0]/60",
                    ),
                    class_name="mb-12",
                ),
                rx.el.div(
                    rx.foreach(CourseState.guitar_courses, _course_card),
                    class_name="grid md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20",
            ),
        ),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Enroll today.",
                        class_name="text-4xl font-bold text-[#F5EFE0] mb-4",
                    ),
                    rx.el.p(
                        "Create a student account and apply to any program.",
                        class_name="text-[#F5EFE0]/70 mb-8",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Register as Student",
                            class_name="px-8 py-4 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
                        ),
                        href="/register",
                    ),
                    class_name="text-center p-16 rounded-3xl bg-gradient-to-br from-[#C9A24B]/10 to-transparent border border-[#C9A24B]/20 backdrop-blur-xl",
                ),
                class_name="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-20",
            ),
        ),
    )
