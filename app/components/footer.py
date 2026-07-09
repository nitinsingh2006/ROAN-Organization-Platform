import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("music", class_name="h-6 w-6 text-[#C9A24B]"),
                        rx.el.span(
                            "ROAN",
                            class_name="text-2xl font-bold text-[#F5EFE0] tracking-widest",
                        ),
                        class_name="flex items-center gap-2 mb-4",
                    ),
                    rx.el.p(
                        "A multi-branch learning universe — where music, culinary arts, technology, and adventure converge.",
                        class_name="text-[#F5EFE0]/60 text-sm max-w-sm leading-relaxed",
                    ),
                    class_name="",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Branches",
                        class_name="text-[#C9A24B] font-semibold mb-4 tracking-wide text-sm uppercase",
                    ),
                    rx.el.a(
                        "Guitar Academy",
                        href="/guitar",
                        class_name="block text-[#F5EFE0]/70 hover:text-[#C9A24B] py-1 text-sm",
                    ),
                    rx.el.a(
                        "Sufiaana Rasoi",
                        href="/sufiaana-rasoi",
                        class_name="block text-[#F5EFE0]/70 hover:text-[#C9A24B] py-1 text-sm",
                    ),
                    rx.el.a(
                        "Infy-X",
                        href="/infy-x",
                        class_name="block text-[#F5EFE0]/70 hover:text-[#C9A24B] py-1 text-sm",
                    ),
                    rx.el.a(
                        "Xplore Trails",
                        href="/xplore-trails",
                        class_name="block text-[#F5EFE0]/70 hover:text-[#C9A24B] py-1 text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.h4(
                        "Company",
                        class_name="text-[#C9A24B] font-semibold mb-4 tracking-wide text-sm uppercase",
                    ),
                    rx.el.a(
                        "About Us",
                        href="/about",
                        class_name="block text-[#F5EFE0]/70 hover:text-[#C9A24B] py-1 text-sm",
                    ),
                    rx.el.a(
                        "Contact",
                        href="/contact",
                        class_name="block text-[#F5EFE0]/70 hover:text-[#C9A24B] py-1 text-sm",
                    ),
                    rx.el.a(
                        "Student Portal",
                        href="/login",
                        class_name="block text-[#F5EFE0]/70 hover:text-[#C9A24B] py-1 text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.h4(
                        "Contact",
                        class_name="text-[#C9A24B] font-semibold mb-4 tracking-wide text-sm uppercase",
                    ),
                    rx.el.p(
                        "hello@roan.edu",
                        class_name="text-[#F5EFE0]/70 text-sm py-1",
                    ),
                    rx.el.p(
                        "+91 98765 43210",
                        class_name="text-[#F5EFE0]/70 text-sm py-1",
                    ),
                    rx.el.p(
                        "Mumbai, India",
                        class_name="text-[#F5EFE0]/70 text-sm py-1",
                    ),
                ),
                class_name="grid grid-cols-2 md:grid-cols-4 gap-8",
            ),
            rx.el.div(
                rx.el.p(
                    "© 2024 ROAN. All rights reserved.",
                    class_name="text-[#F5EFE0]/40 text-sm",
                ),
                rx.el.div(
                    rx.icon(
                        "inbox",
                        class_name="h-5 w-5 text-[#F5EFE0]/60 hover:text-[#C9A24B] cursor-pointer",
                    ),
                    rx.icon(
                        "video",
                        class_name="h-5 w-5 text-[#F5EFE0]/60 hover:text-[#C9A24B] cursor-pointer",
                    ),
                    rx.icon(
                        "wifi",
                        class_name="h-5 w-5 text-[#F5EFE0]/60 hover:text-[#C9A24B] cursor-pointer",
                    ),
                    class_name="flex items-center gap-4",
                ),
                class_name="mt-12 pt-6 border-t border-[#C9A24B]/10 flex flex-col md:flex-row justify-between items-center gap-4",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
        ),
        class_name="bg-[#0A1628] border-t border-[#C9A24B]/10 mt-20",
    )
