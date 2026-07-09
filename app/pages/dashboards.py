import reflex as rx
from app.pages.portals.student import student_dashboard as _student_page
from app.pages.portals.faculty import faculty_dashboard as _faculty_page
from app.pages.portals.institute import institute_dashboard as _institute_page
from app.pages.portals.university import (
    university_dashboard as _university_page,
)
from app.pages.portals.admin import admin_dashboard as _admin_page


def student_dashboard() -> rx.Component:
    return _student_page()


def faculty_dashboard() -> rx.Component:
    return _faculty_page()


def institute_dashboard() -> rx.Component:
    return _institute_page()


def university_dashboard() -> rx.Component:
    return _university_page()


def admin_dashboard() -> rx.Component:
    return _admin_page()
