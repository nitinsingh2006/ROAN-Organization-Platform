import reflex as rx
from app.components.layout import page_shell
from app.states.auth_state import AuthState
from app.components.oauth_buttons import oauth_buttons


def _auth_shell(
    title: str,
    subtitle: str,
    form: rx.Component,
    footer_text: str,
    footer_href: str,
    footer_link: str,
) -> rx.Component:
    return page_shell(
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        subtitle,
                        class_name="text-[#C9A24B] text-xs tracking-[0.3em] font-semibold mb-4 text-center",
                    ),
                    rx.el.h1(
                        title,
                        class_name="text-4xl md:text-5xl font-bold text-[#F5EFE0] mb-8 text-center tracking-tight",
                    ),
                    form,
                    rx.el.p(
                        footer_text,
                        rx.el.a(
                            footer_link,
                            href=footer_href,
                            class_name="text-[#C9A24B] hover:underline ml-1 font-semibold",
                        ),
                        class_name="text-center text-[#F5EFE0]/60 text-sm mt-6",
                    ),
                    class_name="w-full max-w-md",
                ),
                class_name="min-h-[70vh] flex items-center justify-center max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 roan-hero-bg",
            ),
        ),
    )


def login() -> rx.Component:
    return _auth_shell(
        "Welcome back.",
        "STUDENT PORTAL",
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Demo credentials",
                    class_name="text-[#C9A24B] text-xs uppercase tracking-widest font-semibold mb-3",
                ),
                rx.el.div(
                    rx.el.p(
                        "student@roan.edu / student123",
                        class_name="text-[#F5EFE0]/70 text-xs font-mono py-0.5",
                    ),
                    rx.el.p(
                        "faculty@roan.edu / faculty123",
                        class_name="text-[#F5EFE0]/70 text-xs font-mono py-0.5",
                    ),
                    rx.el.p(
                        "institute@roan.edu / institute123",
                        class_name="text-[#F5EFE0]/70 text-xs font-mono py-0.5",
                    ),
                    rx.el.p(
                        "university@roan.edu / university123",
                        class_name="text-[#F5EFE0]/70 text-xs font-mono py-0.5",
                    ),
                    rx.el.p(
                        "admin@roan.edu / admin123",
                        class_name="text-[#F5EFE0]/70 text-xs font-mono py-0.5",
                    ),
                ),
                class_name="p-4 rounded-lg bg-[#C9A24B]/5 border border-[#C9A24B]/20 mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Email",
                        class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                    ),
                    rx.el.input(
                        name="email",
                        type="email",
                        placeholder="you@roan.edu",
                        class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60 transition-all",
                    ),
                    class_name="mb-5",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                    ),
                    rx.el.input(
                        name="password",
                        type="password",
                        placeholder="••••••••",
                        class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60 transition-all",
                    ),
                    class_name="mb-4",
                ),
                rx.cond(
                    AuthState.error != "",
                    rx.el.div(
                        AuthState.error,
                        class_name="p-3 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-sm mb-4",
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    "Sign In",
                    type="submit",
                    class_name="w-full px-8 py-3 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
                ),
                rx.el.a(
                    "Forgot password?",
                    href="/forgot-password",
                    class_name="block text-center text-[#F5EFE0]/50 hover:text-[#C9A24B] text-sm mt-4",
                ),
                oauth_buttons(),
                on_submit=AuthState.login,
                class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] backdrop-blur-xl border border-[#C9A24B]/10 tilt-card",
            ),
        ),
        "Don't have an account?",
        "/register",
        "Register",
    )


def register() -> rx.Component:
    return _auth_shell(
        "Create your account.",
        "JOIN ROAN",
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Full Name",
                    class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                ),
                rx.el.input(
                    name="full_name",
                    placeholder="Your full name",
                    class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60",
                ),
                class_name="mb-4",
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
                    class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                ),
                rx.el.input(
                    name="password",
                    type="password",
                    placeholder="At least 6 characters",
                    class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] placeholder:text-[#F5EFE0]/30 focus:outline-hidden focus:border-[#C9A24B]/60",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Role",
                    class_name="block text-[#F5EFE0]/80 text-sm font-medium mb-2",
                ),
                rx.el.select(
                    rx.el.option("Student", value="student"),
                    rx.el.option("Faculty", value="faculty"),
                    rx.el.option("Institute", value="institute"),
                    name="role",
                    class_name="w-full px-4 py-3 bg-[#F5EFE0]/5 border border-[#C9A24B]/20 rounded-lg text-[#F5EFE0] focus:outline-hidden focus:border-[#C9A24B]/60 appearance-none",
                ),
                class_name="mb-4",
            ),
            rx.cond(
                AuthState.error != "",
                rx.el.div(
                    AuthState.error,
                    class_name="p-3 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-sm mb-4",
                ),
                rx.fragment(),
            ),
            rx.el.button(
                "Create Account",
                type="submit",
                class_name="w-full px-8 py-3 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
            ),
            oauth_buttons(),
            on_submit=AuthState.register,
            class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] backdrop-blur-xl border border-[#C9A24B]/10 tilt-card",
        ),
        "Already have an account?",
        "/login",
        "Sign in",
    )


def forgot() -> rx.Component:
    return _auth_shell(
        "Reset your password.",
        "FORGOT PASSWORD",
        rx.el.div(
            rx.el.p(
                "Password recovery is coming soon. For now, please contact support at hello@roan.edu.",
                class_name="text-[#F5EFE0]/70 text-center mb-6",
            ),
            rx.el.a(
                rx.el.button(
                    "Back to login",
                    class_name="w-full px-8 py-3 bg-[#C9A24B] text-[#0A1628] rounded-lg font-semibold hover:bg-[#C9A24B]/90 transition-all",
                ),
                href="/login",
            ),
            class_name="p-8 rounded-2xl bg-[#F5EFE0]/[0.03] backdrop-blur-xl border border-[#C9A24B]/10",
        ),
        "Remember your password?",
        "/login",
        "Sign in",
    )
