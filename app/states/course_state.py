import reflex as rx
from app.data.seed import get_courses_by_branch, CourseRec


class CourseState(rx.State):
    @rx.var
    def guitar_courses(self) -> list[CourseRec]:
        return get_courses_by_branch("guitar")
