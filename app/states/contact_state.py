import reflex as rx
from app.data.seed import add_contact_message


class ContactState(rx.State):
    status: str = ""
    error: str = ""

    @rx.event
    def submit(self, form_data: dict):
        self.status = ""
        self.error = ""
        name = (form_data.get("name") or "").strip()
        email = (form_data.get("email") or "").strip()
        phone = (form_data.get("phone") or "").strip()
        branch = (form_data.get("branch") or "").strip()
        subject = (form_data.get("subject") or "").strip()
        message = (form_data.get("message") or "").strip()
        if not name or not email or not phone or not branch or not message:
            self.error = "Please fill in all required fields."
            return rx.toast(
                "Please fill in all required fields.", duration=4000
            )
        if "@" not in email or "." not in email:
            self.error = "Please enter a valid email."
            return rx.toast("Please enter a valid email.", duration=4000)
        add_contact_message(
            name=name,
            email=email,
            message=message,
            phone=phone,
            branch=branch,
            subject=subject,
        )
        self.error = ""
        self.status = "Thank you! Your message has been received."
        return rx.toast("Message sent successfully.", duration=4000)
