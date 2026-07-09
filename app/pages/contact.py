import reflex as rx
from app.components.layout import page_shell
from app.states.contact_state import ContactState


def contact() -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "GET IN TOUCH",
                        class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-6",
                    ),
                    rx.el.h1(
                        "Let's ",
                        rx.el.span("talk.", class_name="text-[#C9A24B] italic"),
                        class_name="text-5xl md:text-7xl font-bold text-[#F5EFE0] tracking-tight mb-6",
                    ),
                    rx.el.p(
                        "Questions about programs, partnerships, or press? Drop us a line.",
                        class_name="text-lg text-[#F5EFE0]/70 max-w-xl mb-12",
                    ),
                ),
                rx.el.div(
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "Name",
                                class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                            ),
                            rx.el.input(
                                name="name",
                                placeholder="Your name",
                                class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60 transition-all",
                            ),
                            class_name="mb-5",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email",
                                class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                            ),
                            rx.el.input(
                                name="email",
                                type="email",
                                placeholder="you@example.com",
                                class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60 transition-all",
                            ),
                            class_name="mb-5",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Phone",
                                class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                            ),
                            rx.el.input(
                                name="phone",
                                placeholder="+91 98765 43210",
                                class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60 transition-all",
                            ),
                            class_name="mb-5",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Branch of Interest",
                                class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                            ),
                            rx.el.select(
                                rx.el.option(
                                    "Select a branch",
                                    value="",
                                    disabled=True,
                                ),
                                rx.el.option(
                                    "Guitar Academy", value="Guitar Academy"
                                ),
                                rx.el.option(
                                    "Sufiaana Rasoi", value="Sufiaana Rasoi"
                                ),
                                rx.el.option("Infy-X", value="Infy-X"),
                                rx.el.option(
                                    "Xplore Trails", value="Xplore Trails"
                                ),
                                rx.el.option("General", value="General"),
                                name="branch",
                                default_value="",
                                class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] focus:outline-hidden focus:border-[#C9A24B]/60 transition-all appearance-none",
                            ),
                            class_name="mb-5",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Subject",
                                class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                            ),
                            rx.el.input(
                                name="subject",
                                placeholder="What is this about? (optional)",
                                class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60 transition-all",
                            ),
                            class_name="mb-5",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Message",
                                class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                            ),
                            rx.el.textarea(
                                name="message",
                                placeholder="Tell us more...",
                                rows="5",
                                class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60 transition-all resize-none",
                            ),
                            class_name="mb-6",
                        ),
                        rx.cond(
                            ContactState.error != "",
                            rx.el.div(
                                rx.icon("triangle-alert", class_name="h-4 w-4"),
                                rx.el.span(
                                    ContactState.error, class_name="text-sm"
                                ),
                                class_name="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg mb-4",
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            ContactState.status != "",
                            rx.el.div(
                                rx.icon("circle-check", class_name="h-4 w-4"),
                                rx.el.span(
                                    ContactState.status, class_name="text-sm"
                                ),
                                class_name="flex items-center gap-2 p-3 bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg mb-4",
                            ),
                            rx.fragment(),
                        ),
                        rx.el.button(
                            "Send Message",
                            rx.icon("send", class_name="h-4 w-4"),
                            type="submit",
                            class_name="flex items-center gap-2 px-8 py-4 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
                        ),
                        on_submit=ContactState.submit,
                        reset_on_submit=True,
                        class_name="p-8 md:p-10 rounded-2xl bg-[#F5EFE0]/[0.03] backdrop-blur-xl border border-[#C9A24B]/10",
                    ),
                    class_name="max-w-2xl",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
            ),
        ),
    )
