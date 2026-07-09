import reflex as rx
from app.pages.home import home
from app.pages.guitar import guitar
from app.pages.coming_soon import sufiaana, infyx, xplore
from app.pages.about import about
from app.pages.contact import contact
from app.pages.auth import login, register, forgot
from app.pages.errors import not_found, not_authorized
from app.pages.dashboards import (
    student_dashboard,
    faculty_dashboard,
    institute_dashboard,
    university_dashboard,
    admin_dashboard,
)
from app.states.auth_state import AuthState
from app.states.student_state import StudentState
from app.states.oauth_state import OAuthState
from app.pages.oauth_callback import google_callback, github_callback


def index() -> rx.Component:
    return home()


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/roan_effects.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
    style={"background": "#0A1628"},
)

app.add_page(index, route="/")
app.add_page(guitar, route="/guitar")
app.add_page(sufiaana, route="/sufiaana-rasoi")
app.add_page(infyx, route="/infy-x")
app.add_page(xplore, route="/xplore-trails")
app.add_page(about, route="/about")
app.add_page(contact, route="/contact")
app.add_page(login, route="/login")
app.add_page(register, route="/register")
app.add_page(forgot, route="/forgot-password")
app.add_page(not_authorized, route="/not-authorized")
app.add_page(not_found, route="/404")

app.add_page(
    student_dashboard,
    route="/portal/student",
    on_load=[AuthState.guard_student, StudentState.load],
)
app.add_page(
    faculty_dashboard, route="/portal/faculty", on_load=AuthState.guard_faculty
)
app.add_page(
    institute_dashboard,
    route="/portal/institute",
    on_load=AuthState.guard_institute,
)
app.add_page(
    university_dashboard,
    route="/portal/university",
    on_load=AuthState.guard_university,
)
app.add_page(
    admin_dashboard, route="/portal/admin", on_load=AuthState.guard_admin
)
app.add_page(
    google_callback,
    route="/auth/callback/google",
    on_load=OAuthState.handle_google_callback,
)
app.add_page(
    github_callback,
    route="/auth/callback/github",
    on_load=OAuthState.handle_github_callback,
)
