import reflex as rx
from app.data.seed import find_user, verify_password, register_user

ROLE_ROUTES: dict[str, str] = {
    "student": "/portal/student",
    "faculty": "/portal/faculty",
    "institute": "/portal/institute",
    "university": "/portal/university",
    "super_admin": "/portal/admin",
}


class AuthState(rx.State):
    user_id: int = 0
    user_email: str = ""
    user_name: str = ""
    user_role: str = ""
    error: str = ""
    success: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user_id > 0

    @rx.event
    def login(self, form_data: dict):
        self.error = ""
        self.success = ""
        email = (form_data.get("email") or "").strip()
        password = form_data.get("password") or ""
        if not email or not password:
            self.error = "Email and password are required."
            return
        user = find_user(email)
        if not user or not verify_password(user, password):
            self.error = "Invalid email or password."
            return
        if not user["is_active"]:
            self.error = (
                "This account is inactive. Please contact administration."
            )
            return
        self.user_id = user["id"]
        self.user_email = user["email"]
        self.user_name = user["full_name"]
        self.user_role = user["role"]
        return rx.redirect(ROLE_ROUTES.get(user["role"], "/"))

    @rx.event
    def register(self, form_data: dict):
        self.error = ""
        self.success = ""
        email = (form_data.get("email") or "").strip()
        password = form_data.get("password") or ""
        full_name = (form_data.get("full_name") or "").strip()
        role = form_data.get("role") or "student"
        if not email or not password or not full_name:
            self.error = "All fields are required."
            return
        if len(password) < 6:
            self.error = "Password must be at least 6 characters."
            return
        user = register_user(email, password, full_name, role)
        if user is None:
            self.error = "An account with this email already exists."
            return
        self.success = "Account created successfully. Please log in."
        return rx.redirect("/login")

    @rx.event
    def logout(self):
        self.user_id = 0
        self.user_email = ""
        self.user_name = ""
        self.user_role = ""
        self.error = ""
        self.success = ""
        return rx.redirect("/")

    @rx.event
    def require_role(self, allowed: list[str]):
        if self.user_id == 0:
            return rx.redirect("/login")
        if self.user_role not in allowed:
            return rx.redirect("/not-authorized")
        return None

    @rx.event
    def guard_student(self):
        return AuthState.require_role(["student"])

    @rx.event
    def guard_faculty(self):
        return AuthState.require_role(["faculty"])

    @rx.event
    def guard_institute(self):
        return AuthState.require_role(["institute"])

    @rx.event
    def guard_university(self):
        return AuthState.require_role(["university"])

    @rx.event
    def guard_admin(self):
        return AuthState.require_role(["super_admin"])
