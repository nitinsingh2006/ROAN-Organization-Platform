import hashlib
from datetime import datetime, timedelta
from typing import TypedDict
import logging


def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def _now_str() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M")


class UserRec(TypedDict):
    id: int
    email: str
    password_hash: str
    role: str
    full_name: str
    is_active: bool


class CourseRec(TypedDict):
    id: int
    branch: str
    title: str
    level: str
    duration: str
    fee: float
    description: str
    seats: int


class ContactRec(TypedDict):
    id: int
    name: str
    email: str
    phone: str
    branch: str
    subject: str
    message: str
    created_at: str
    submitted_date: str
    is_read: bool
    is_responded: bool


ROLES: list[str] = [
    "student",
    "faculty",
    "institute",
    "university",
    "super_admin",
]

USERS: list[UserRec] = [
    {
        "id": 1,
        "email": "student@roan.edu",
        "password_hash": _hash("student123"),
        "role": "student",
        "full_name": "Aarav Sharma",
        "is_active": True,
    },
    {
        "id": 2,
        "email": "faculty@roan.edu",
        "password_hash": _hash("faculty123"),
        "role": "faculty",
        "full_name": "Priya Menon",
        "is_active": True,
    },
    {
        "id": 3,
        "email": "institute@roan.edu",
        "password_hash": _hash("institute123"),
        "role": "institute",
        "full_name": "Rahul Verma",
        "is_active": True,
    },
    {
        "id": 4,
        "email": "university@roan.edu",
        "password_hash": _hash("university123"),
        "role": "university",
        "full_name": "Dr. Anjali Rao",
        "is_active": True,
    },
    {
        "id": 5,
        "email": "admin@roan.edu",
        "password_hash": _hash("admin123"),
        "role": "super_admin",
        "full_name": "Kabir Singh",
        "is_active": True,
    },
    {
        "id": 6,
        "email": "inactive@roan.edu",
        "password_hash": _hash("inactive123"),
        "role": "student",
        "full_name": "Inactive User",
        "is_active": False,
    },
]

COURSES: list[CourseRec] = [
    {
        "id": 1,
        "branch": "guitar",
        "title": "Foundations of Acoustic Guitar",
        "level": "Beginner",
        "duration": "3 Months",
        "fee": 8500.0,
        "description": "Master posture, chords, strumming patterns, and your first songs on an acoustic guitar.",
        "seats": 24,
    },
    {
        "id": 2,
        "branch": "guitar",
        "title": "Fingerstyle & Melody Craft",
        "level": "Intermediate",
        "duration": "4 Months",
        "fee": 12500.0,
        "description": "Develop fingerpicking, arpeggios, and melodic phrasing across popular and classical styles.",
        "seats": 18,
    },
    {
        "id": 3,
        "branch": "guitar",
        "title": "Electric Guitar & Blues Rock",
        "level": "Intermediate",
        "duration": "5 Months",
        "fee": 14500.0,
        "description": "Amp basics, tone shaping, blues scales, rock riffs, and improvisation over backing tracks.",
        "seats": 16,
    },
    {
        "id": 4,
        "branch": "guitar",
        "title": "Advanced Lead & Improvisation",
        "level": "Advanced",
        "duration": "6 Months",
        "fee": 18500.0,
        "description": "Modes, chord-tone soloing, sweep picking, and stage-ready improvisation.",
        "seats": 12,
    },
    {
        "id": 5,
        "branch": "guitar",
        "title": "Songwriting on Guitar",
        "level": "All Levels",
        "duration": "2 Months",
        "fee": 6500.0,
        "description": "Turn chord progressions into complete songs — lyrics, structure, and recording basics.",
        "seats": 20,
    },
    {
        "id": 6,
        "branch": "guitar",
        "title": "Classical Guitar Diploma",
        "level": "Advanced",
        "duration": "12 Months",
        "fee": 32000.0,
        "description": "University-affiliated diploma covering classical repertoire, sight-reading, and performance.",
        "seats": 10,
    },
]


class EnrollmentRec(TypedDict):
    id: int
    student_id: int
    course_id: int
    status: str
    enrolled_at: str


class ExamRec(TypedDict):
    id: int
    course_id: int
    title: str
    exam_date: str
    application_deadline: str
    mode: str
    venue: str
    max_marks: int


class ExamApplicationRec(TypedDict):
    id: int
    exam_id: int
    student_id: int
    status: str
    applied_at: str
    mode: str
    institute_recommended_mode: str
    fee_paid: bool


class ResultRec(TypedDict):
    id: int
    exam_id: int
    student_id: int
    marks: float
    max_marks: int
    grade: str
    declared_at: str
    declared: bool


class DocumentRec(TypedDict):
    id: int
    student_id: int
    doc_type: str
    file_name: str
    status: str
    uploaded_at: str
    reviewer_note: str


class NotificationRec(TypedDict):
    id: int
    user_id: int
    title: str
    body: str
    created_at: str
    is_read: bool


class AttendanceRec(TypedDict):
    id: int
    course_id: int
    student_id: int
    date: str
    status: str
    marked_by: int


class AssessmentRec(TypedDict):
    id: int
    course_id: int
    student_id: int
    title: str
    marks: float
    max_marks: float
    remarks: str
    graded_by: int
    graded_at: str


class PracticalRec(TypedDict):
    id: int
    course_id: int
    student_id: int
    title: str
    grade: str
    remarks: str
    graded_by: int
    graded_at: str


class FeeRec(TypedDict):
    id: int
    student_id: int
    course_id: int
    amount: float
    status: str
    updated_at: str
    updated_by: int


class CertificateRec(TypedDict):
    id: int
    student_id: int
    course_id: int
    title: str
    issued_at: str
    status: str


class StudentProfileRec(TypedDict):
    user_id: int
    phone: str
    address: str
    date_of_birth: str
    guardian: str


class AuditLogRec(TypedDict):
    id: int
    actor_id: int
    actor_role: str
    action: str
    target_type: str
    target_id: int
    detail: str
    created_at: str


AUDIT_LOGS: list[AuditLogRec] = []
_audit_id_counter = [0]


def add_audit_log(
    actor_id: int,
    actor_role: str,
    action: str,
    target_type: str,
    target_id: int,
    detail: str,
) -> AuditLogRec:
    _audit_id_counter[0] += 1
    rec: AuditLogRec = {
        "id": _audit_id_counter[0],
        "actor_id": actor_id,
        "actor_role": actor_role,
        "action": action,
        "target_type": target_type,
        "target_id": target_id,
        "detail": detail,
        "created_at": _now_str(),
    }
    AUDIT_LOGS.append(rec)
    return rec


CONTACT_MESSAGES: list[ContactRec] = []
_contact_id_counter = [0]


def add_contact_message(
    name: str,
    email: str,
    message: str,
    phone: str = "",
    branch: str = "",
    subject: str = "",
) -> ContactRec:
    from datetime import datetime

    _contact_id_counter[0] += 1
    now = datetime.utcnow()
    rec: ContactRec = {
        "id": _contact_id_counter[0],
        "name": name,
        "email": email,
        "phone": phone,
        "branch": branch,
        "subject": subject,
        "message": message,
        "created_at": now.strftime("%Y-%m-%d %H:%M"),
        "submitted_date": now.strftime("%Y-%m-%d"),
        "is_read": False,
        "is_responded": False,
    }
    CONTACT_MESSAGES.append(rec)
    return rec


def find_user(email: str) -> UserRec | None:
    for u in USERS:
        if u["email"].lower() == email.lower():
            return u
    return None


def verify_password(user: UserRec, password: str) -> bool:
    return user["password_hash"] == _hash(password)


_user_id_counter = [len(USERS)]


def _next_user_id() -> int:
    max_id = max((u["id"] for u in USERS), default=0)
    max_seen = max(max_id, _user_id_counter[0], _counters.get("user", 0))
    _user_id_counter[0] = max_seen + 1
    _counters["user"] = _user_id_counter[0]
    return _user_id_counter[0]


def register_user(
    email: str, password: str, full_name: str, role: str
) -> UserRec | None:
    if find_user(email):
        return None
    new_id = _next_user_id()
    rec: UserRec = {
        "id": new_id,
        "email": email,
        "password_hash": _hash(password),
        "role": role,
        "full_name": full_name,
        "is_active": True,
    }
    USERS.append(rec)
    return rec


OAUTH_LINKS: list[dict[str, str | int]] = []


def link_or_create_oauth_user(
    provider: str, provider_uid: str, email: str, full_name: str
) -> UserRec | None:
    if not email:
        return None
    # Check existing OAuth link
    for link in OAUTH_LINKS:
        if (
            link["provider"] == provider
            and link["provider_uid"] == provider_uid
        ):
            return find_user_by_id(int(link["user_id"]))
    # Match by email
    user = find_user(email)
    if user is not None:
        OAUTH_LINKS.append(
            {
                "provider": provider,
                "provider_uid": provider_uid,
                "user_id": user["id"],
                "email": email,
            }
        )
        return user
    # Create new student
    new_id = _next_user_id()
    rec: UserRec = {
        "id": new_id,
        "email": email,
        "password_hash": _hash("!oauth!"),
        "role": "student",
        "full_name": full_name or email.split("@")[0].title(),
        "is_active": True,
    }
    USERS.append(rec)
    STUDENT_PROFILES.append(
        {
            "user_id": new_id,
            "phone": "",
            "address": "",
            "date_of_birth": "",
            "guardian": "",
        }
    )
    OAUTH_LINKS.append(
        {
            "provider": provider,
            "provider_uid": provider_uid,
            "user_id": new_id,
            "email": email,
        }
    )
    push_notification(
        new_id,
        "Welcome to ROAN",
        f"Your account was created via {provider.title()} sign-in.",
    )
    return rec


def get_courses_by_branch(branch: str) -> list[CourseRec]:
    return [c for c in COURSES if c["branch"] == branch]


ENROLLMENTS: list[EnrollmentRec] = []
EXAMS: list[ExamRec] = []
EXAM_APPLICATIONS: list[ExamApplicationRec] = []
RESULTS: list[ResultRec] = []
DOCUMENTS: list[DocumentRec] = []
NOTIFICATIONS: list[NotificationRec] = []
ATTENDANCE: list[AttendanceRec] = []
ASSESSMENTS: list[AssessmentRec] = []
PRACTICALS: list[PracticalRec] = []
FEES: list[FeeRec] = []
CERTIFICATES: list[CertificateRec] = []
STUDENT_PROFILES: list[StudentProfileRec] = []

_counters: dict[str, int] = {
    "enrollment": 0,
    "exam": 0,
    "exam_app": 0,
    "result": 0,
    "document": 0,
    "notification": 0,
    "attendance": 0,
    "assessment": 0,
    "practical": 0,
    "fee": 0,
    "certificate": 0,
    "user": len(USERS),
}


def _next(key: str) -> int:
    _counters[key] += 1
    return _counters[key]


def _seed_students() -> None:
    demo_students = [
        ("aarav.student@roan.edu", "Aarav Sharma"),
        ("meera.student@roan.edu", "Meera Iyer"),
        ("kabir.student@roan.edu", "Kabir Khan"),
        ("nisha.student@roan.edu", "Nisha Rao"),
        ("dev.student@roan.edu", "Dev Patel"),
    ]
    for email, name in demo_students:
        if find_user(email) is None:
            _counters["user"] += 1
            USERS.append(
                {
                    "id": _counters["user"],
                    "email": email,
                    "password_hash": _hash("student123"),
                    "role": "student",
                    "full_name": name,
                    "is_active": True,
                }
            )
    for u in USERS:
        if u["role"] == "student":
            if not any(sp["user_id"] == u["id"] for sp in STUDENT_PROFILES):
                STUDENT_PROFILES.append(
                    {
                        "user_id": u["id"],
                        "phone": "+91 98765 " + str(10000 + u["id"]),
                        "address": "Mumbai, India",
                        "date_of_birth": "2001-01-15",
                        "guardian": "Guardian of " + u["full_name"],
                    }
                )


def _seed_exams() -> None:
    today = datetime.utcnow()
    for c in COURSES:
        eid = _next("exam")
        EXAMS.append(
            {
                "id": eid,
                "course_id": c["id"],
                "title": f"{c['title']} - Term Exam",
                "exam_date": (
                    today + timedelta(days=30 + c["id"] * 3)
                ).strftime("%Y-%m-%d"),
                "application_deadline": (
                    today + timedelta(days=10 + c["id"])
                ).strftime("%Y-%m-%d"),
                "mode": "Offline",
                "venue": "ROAN Main Campus, Mumbai",
                "max_marks": 100,
            }
        )
    # one past-deadline exam
    eid = _next("exam")
    EXAMS.append(
        {
            "id": eid,
            "course_id": COURSES[0]["id"],
            "title": "Foundations Guitar - Special Exam (Closed)",
            "exam_date": (today - timedelta(days=5)).strftime("%Y-%m-%d"),
            "application_deadline": (today - timedelta(days=15)).strftime(
                "%Y-%m-%d"
            ),
            "mode": "Offline",
            "venue": "ROAN Main Campus, Mumbai",
            "max_marks": 100,
        }
    )


def _seed_dynamic() -> None:
    students = [u for u in USERS if u["role"] == "student"]
    if not students:
        return
    s1 = students[0]
    s2 = students[1] if len(students) > 1 else s1
    # Enrollments
    e_id = _next("enrollment")
    ENROLLMENTS.append(
        {
            "id": e_id,
            "student_id": s1["id"],
            "course_id": COURSES[0]["id"],
            "status": "active",
            "enrolled_at": _now_str(),
        }
    )
    e_id = _next("enrollment")
    ENROLLMENTS.append(
        {
            "id": e_id,
            "student_id": s1["id"],
            "course_id": COURSES[1]["id"],
            "status": "active",
            "enrolled_at": _now_str(),
        }
    )
    e_id = _next("enrollment")
    ENROLLMENTS.append(
        {
            "id": e_id,
            "student_id": s2["id"],
            "course_id": COURSES[0]["id"],
            "status": "active",
            "enrolled_at": _now_str(),
        }
    )
    # Documents
    d_id = _next("document")
    DOCUMENTS.append(
        {
            "id": d_id,
            "student_id": s1["id"],
            "doc_type": "ID Proof",
            "file_name": "aadhaar.pdf",
            "status": "verified",
            "uploaded_at": _now_str(),
            "reviewer_note": "Verified successfully.",
        }
    )
    d_id = _next("document")
    DOCUMENTS.append(
        {
            "id": d_id,
            "student_id": s1["id"],
            "doc_type": "Photo",
            "file_name": "photo.jpg",
            "status": "pending",
            "uploaded_at": _now_str(),
            "reviewer_note": "",
        }
    )
    d_id = _next("document")
    DOCUMENTS.append(
        {
            "id": d_id,
            "student_id": s2["id"],
            "doc_type": "ID Proof",
            "file_name": "pan.pdf",
            "status": "pending",
            "uploaded_at": _now_str(),
            "reviewer_note": "",
        }
    )
    # Notifications
    for st in students[:3]:
        n_id = _next("notification")
        NOTIFICATIONS.append(
            {
                "id": n_id,
                "user_id": st["id"],
                "title": "Welcome to ROAN",
                "body": "Your student portal is now active. Explore courses and apply for exams.",
                "created_at": _now_str(),
                "is_read": False,
            }
        )
    # Fees
    f_id = _next("fee")
    FEES.append(
        {
            "id": f_id,
            "student_id": s1["id"],
            "course_id": COURSES[0]["id"],
            "amount": COURSES[0]["fee"],
            "status": "paid",
            "updated_at": _now_str(),
            "updated_by": 3,
        }
    )
    f_id = _next("fee")
    FEES.append(
        {
            "id": f_id,
            "student_id": s1["id"],
            "course_id": COURSES[1]["id"],
            "amount": COURSES[1]["fee"],
            "status": "pending",
            "updated_at": _now_str(),
            "updated_by": 3,
        }
    )
    f_id = _next("fee")
    FEES.append(
        {
            "id": f_id,
            "student_id": s2["id"],
            "course_id": COURSES[0]["id"],
            "amount": COURSES[0]["fee"],
            "status": "pending",
            "updated_at": _now_str(),
            "updated_by": 3,
        }
    )
    # Results
    r_id = _next("result")
    RESULTS.append(
        {
            "id": r_id,
            "exam_id": EXAMS[-1]["id"],
            "student_id": s1["id"],
            "marks": 82.0,
            "max_marks": 100,
            "grade": "A",
            "declared_at": _now_str(),
            "declared": True,
        }
    )
    # Certificates
    c_id = _next("certificate")
    CERTIFICATES.append(
        {
            "id": c_id,
            "student_id": s1["id"],
            "course_id": COURSES[0]["id"],
            "title": "Foundations of Acoustic Guitar - Completion",
            "issued_at": _now_str(),
            "status": "issued",
        }
    )


_seed_students()
_seed_exams()
_seed_dynamic()


def push_notification(user_id: int, title: str, body: str) -> None:
    _counters["notification"] += 1
    NOTIFICATIONS.append(
        {
            "id": _counters["notification"],
            "user_id": user_id,
            "title": title,
            "body": body,
            "created_at": _now_str(),
            "is_read": False,
        }
    )


def _seed_applications() -> None:
    """Seed exam applications across all workflow statuses.

    Ensures the persistent data layer initializes with:
    - At least one pending application
    - At least one forwarded application (ready for university review)
    - At least one approved application with ALL admit-card prerequisites
      satisfied (course fee paid, ID document verified)
    - At least one rejected application
    Plus related notifications and audit-log entries.
    """
    students = [u for u in USERS if u["role"] == "student"]
    if not students or not EXAMS:
        return

    # Guarantee we have enough students and enrollments to build realistic apps.
    # Use up to four distinct students; enroll them in appropriate courses.
    demo_students = students[:5]

    # Helper: ensure enrollment exists (active) for a student in a course.
    def _ensure_enrollment(sid: int, cid: int) -> None:
        for e in ENROLLMENTS:
            if e["student_id"] == sid and e["course_id"] == cid:
                e["status"] = "active"
                return
        _counters["enrollment"] += 1
        ENROLLMENTS.append(
            {
                "id": _counters["enrollment"],
                "student_id": sid,
                "course_id": cid,
                "status": "active",
                "enrolled_at": _now_str(),
            }
        )

    # Helper: ensure a fee record exists with a specific status.
    def _ensure_fee(sid: int, cid: int, status: str) -> None:
        course = find_course(cid)
        amount = course["fee"] if course else 0.0
        for f in FEES:
            if f["student_id"] == sid and f["course_id"] == cid:
                f["status"] = status
                f["updated_at"] = _now_str()
                return
        _counters["fee"] += 1
        FEES.append(
            {
                "id": _counters["fee"],
                "student_id": sid,
                "course_id": cid,
                "amount": amount,
                "status": status,
                "updated_at": _now_str(),
                "updated_by": 3,
            }
        )

    # Helper: ensure an ID document exists with a specific status.
    def _ensure_id_doc(sid: int, status: str, file_name: str) -> None:
        for d in DOCUMENTS:
            if d["student_id"] == sid and d["doc_type"] == "ID Proof":
                d["status"] = status
                d["file_name"] = file_name
                d["reviewer_note"] = (
                    "Verified by institute."
                    if status == "verified"
                    else d["reviewer_note"]
                )
                return
        _counters["document"] += 1
        DOCUMENTS.append(
            {
                "id": _counters["document"],
                "student_id": sid,
                "doc_type": "ID Proof",
                "file_name": file_name,
                "status": status,
                "uploaded_at": _now_str(),
                "reviewer_note": (
                    "Verified by institute." if status == "verified" else ""
                ),
            }
        )

    # Helper: create an exam application with given status.
    def _create_app(
        sid: int, exam_id: int, status: str, recommended: str, fee_paid: bool
    ) -> ExamApplicationRec:
        exam = find_exam(exam_id)
        mode = exam["mode"] if exam else "Offline"
        _counters["exam_app"] += 1
        rec: ExamApplicationRec = {
            "id": _counters["exam_app"],
            "exam_id": exam_id,
            "student_id": sid,
            "status": status,
            "applied_at": _now_str(),
            "mode": mode,
            "institute_recommended_mode": recommended,
            "fee_paid": fee_paid,
        }
        EXAM_APPLICATIONS.append(rec)
        return rec

    # Pick a set of valid, in-window exams (deadline not yet passed).
    from datetime import datetime as _dt

    now = _dt.utcnow()
    open_exams: list[ExamRec] = []
    for ex in EXAMS:
        try:
            deadline = _dt.strptime(ex["application_deadline"], "%Y-%m-%d")
            if deadline >= now:
                open_exams.append(ex)
        except Exception:
            logging.exception("Unexpected error")
            continue
    if not open_exams:
        open_exams = list(EXAMS)

    # Distribute up to four exams for the four canonical statuses.
    def _pick_exam(i: int) -> ExamRec:
        return open_exams[i % len(open_exams)]

    exam_pending = _pick_exam(0)
    exam_forwarded = _pick_exam(1)
    exam_approved = _pick_exam(2)
    exam_rejected = _pick_exam(3)

    # ---- 1) Pending application ----
    s_pending = demo_students[0]
    _ensure_enrollment(s_pending["id"], exam_pending["course_id"])
    _ensure_fee(s_pending["id"], exam_pending["course_id"], "pending")
    _ensure_id_doc(s_pending["id"], "pending", "id_pending.pdf")
    app_pending = _create_app(
        s_pending["id"], exam_pending["id"], "pending", "", False
    )
    push_notification(
        s_pending["id"],
        "Exam application received",
        f"Your application for '{exam_pending['title']}' is pending institute review.",
    )

    # ---- 2) Forwarded application (ready for university review) ----
    s_fwd = demo_students[1] if len(demo_students) > 1 else s_pending
    _ensure_enrollment(s_fwd["id"], exam_forwarded["course_id"])
    _ensure_fee(s_fwd["id"], exam_forwarded["course_id"], "paid")
    _ensure_id_doc(s_fwd["id"], "verified", "id_verified_fwd.pdf")
    app_fwd = _create_app(
        s_fwd["id"], exam_forwarded["id"], "forwarded", "Offline", False
    )
    push_notification(
        s_fwd["id"],
        "Application forwarded",
        f"Your application for '{exam_forwarded['title']}' has been forwarded to the University.",
    )
    add_audit_log(
        3,
        "institute",
        "recommend_exam_mode",
        "exam_application",
        app_fwd["id"],
        "Recommended Offline mode",
    )

    # ---- 3) Approved application with FULL admit-card prerequisites ----
    s_approved = demo_students[2] if len(demo_students) > 2 else s_pending
    _ensure_enrollment(s_approved["id"], exam_approved["course_id"])
    _ensure_fee(s_approved["id"], exam_approved["course_id"], "paid")
    _ensure_id_doc(s_approved["id"], "verified", "id_verified_approved.pdf")
    app_approved = _create_app(
        s_approved["id"], exam_approved["id"], "approved", "Offline", True
    )
    push_notification(
        s_approved["id"],
        "Exam application approved",
        f"Your application for '{exam_approved['title']}' has been approved. Admit card available.",
    )
    add_audit_log(
        4,
        "university",
        "approve_application",
        "exam_application",
        app_approved["id"],
        "Approved by University — prerequisites verified.",
    )

    # ---- 4) Rejected application ----
    s_rejected = demo_students[3] if len(demo_students) > 3 else s_pending
    _ensure_enrollment(s_rejected["id"], exam_rejected["course_id"])
    _ensure_fee(s_rejected["id"], exam_rejected["course_id"], "pending")
    _ensure_id_doc(s_rejected["id"], "rejected", "id_unclear.jpg")
    app_rejected = _create_app(
        s_rejected["id"], exam_rejected["id"], "rejected", "Offline", False
    )
    push_notification(
        s_rejected["id"],
        "Exam application rejected",
        f"Your application for '{exam_rejected['title']}' was rejected. Please contact your institute.",
    )
    add_audit_log(
        4,
        "university",
        "reject_application",
        "exam_application",
        app_rejected["id"],
        "Rejected — document verification failed.",
    )

    # ---- 5) Extra forwarded application to keep the University queue populated ----
    if len(demo_students) > 4 and len(open_exams) > 1:
        s_extra = demo_students[4]
        exam_extra = _pick_exam(4)
        _ensure_enrollment(s_extra["id"], exam_extra["course_id"])
        _ensure_fee(s_extra["id"], exam_extra["course_id"], "paid")
        _ensure_id_doc(s_extra["id"], "verified", "id_extra_verified.pdf")
        app_extra = _create_app(
            s_extra["id"], exam_extra["id"], "forwarded", "Online", False
        )
        push_notification(
            s_extra["id"],
            "Application forwarded",
            f"Your application for '{exam_extra['title']}' has been forwarded to the University.",
        )
        add_audit_log(
            3,
            "institute",
            "recommend_exam_mode",
            "exam_application",
            app_extra["id"],
            "Recommended Online mode",
        )


def find_user_by_id(uid: int) -> UserRec | None:
    for u in USERS:
        if u["id"] == uid:
            return u
    return None


def find_course(cid: int) -> CourseRec | None:
    for c in COURSES:
        if c["id"] == cid:
            return c
    return None


def find_exam(eid: int) -> ExamRec | None:
    for e in EXAMS:
        if e["id"] == eid:
            return e
    return None


# Bind local reference so the helper can find `seed` (self) safely; not required
# but keeps _seed_applications self-contained.
seed_module = None  # placeholder to avoid NameError if referenced
del seed_module

_seed_applications()


def student_enrollments(sid: int) -> list[EnrollmentRec]:
    return [e for e in ENROLLMENTS if e["student_id"] == sid]


def student_active_course_ids(sid: int) -> list[int]:
    return [
        e["course_id"]
        for e in ENROLLMENTS
        if e["student_id"] == sid and e["status"] == "active"
    ]


def enroll_student(sid: int, cid: int) -> tuple[bool, str]:
    for e in ENROLLMENTS:
        if (
            e["student_id"] == sid
            and e["course_id"] == cid
            and e["status"] == "active"
        ):
            return False, "You are already enrolled in this course."
    _counters["enrollment"] += 1
    ENROLLMENTS.append(
        {
            "id": _counters["enrollment"],
            "student_id": sid,
            "course_id": cid,
            "status": "active",
            "enrolled_at": _now_str(),
        }
    )
    course = find_course(cid)
    if course is not None:
        _counters["fee"] += 1
        FEES.append(
            {
                "id": _counters["fee"],
                "student_id": sid,
                "course_id": cid,
                "amount": course["fee"],
                "status": "pending",
                "updated_at": _now_str(),
                "updated_by": 0,
            }
        )
    return True, "Enrolled successfully."


def drop_enrollment(sid: int, cid: int) -> tuple[bool, str]:
    for e in ENROLLMENTS:
        if (
            e["student_id"] == sid
            and e["course_id"] == cid
            and e["status"] == "active"
        ):
            e["status"] = "dropped"
            return True, "You have dropped this course."
    return False, "You are not enrolled in this course."


def apply_for_exam(sid: int, exam_id: int) -> tuple[bool, str]:
    exam = find_exam(exam_id)
    if exam is None:
        return False, "Exam not found."
    try:
        deadline = datetime.strptime(exam["application_deadline"], "%Y-%m-%d")
    except Exception:
        logging.exception("Unexpected error")
        deadline = datetime.utcnow() + timedelta(days=30)
    if datetime.utcnow() > deadline + timedelta(days=1):
        return False, "The application deadline has passed."
    for a in EXAM_APPLICATIONS:
        if a["exam_id"] == exam_id and a["student_id"] == sid:
            return False, "You have already applied for this exam."
    if exam["course_id"] not in student_active_course_ids(sid):
        return False, "You must be enrolled in the related course."
    _counters["exam_app"] += 1
    EXAM_APPLICATIONS.append(
        {
            "id": _counters["exam_app"],
            "exam_id": exam_id,
            "student_id": sid,
            "status": "pending",
            "applied_at": _now_str(),
            "mode": exam["mode"],
            "institute_recommended_mode": "",
            "fee_paid": False,
        }
    )
    return True, "Exam application submitted."


def upload_document(
    sid: int, doc_type: str, file_name: str
) -> tuple[bool, str]:
    allowed_ext = {"pdf", "jpg", "jpeg", "png"}
    ext = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
    if ext not in allowed_ext:
        return False, "Only PDF/JPG/JPEG/PNG files under 5 MB are accepted."
    _counters["document"] += 1
    DOCUMENTS.append(
        {
            "id": _counters["document"],
            "student_id": sid,
            "doc_type": doc_type,
            "file_name": file_name,
            "status": "pending",
            "uploaded_at": _now_str(),
            "reviewer_note": "",
        }
    )
    return True, "Document uploaded and awaiting verification."


def mark_notification_read(nid: int, user_id: int) -> None:
    for n in NOTIFICATIONS:
        if n["id"] == nid and n["user_id"] == user_id:
            n["is_read"] = True
            return


def update_profile(
    user_id: int, full_name: str, phone: str, address: str
) -> None:
    for u in USERS:
        if u["id"] == user_id and full_name:
            u["full_name"] = full_name
    for sp in STUDENT_PROFILES:
        if sp["user_id"] == user_id:
            sp["phone"] = phone or sp["phone"]
            sp["address"] = address or sp["address"]
            return
    STUDENT_PROFILES.append(
        {
            "user_id": user_id,
            "phone": phone,
            "address": address,
            "date_of_birth": "",
            "guardian": "",
        }
    )


def student_profile(user_id: int) -> StudentProfileRec | None:
    for sp in STUDENT_PROFILES:
        if sp["user_id"] == user_id:
            return sp
    return None


def admit_card_eligibility(sid: int, exam_id: int) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    exam = find_exam(exam_id)
    if exam is None:
        return False, ["Exam not found."]
    app = next(
        (
            a
            for a in EXAM_APPLICATIONS
            if a["exam_id"] == exam_id and a["student_id"] == sid
        ),
        None,
    )
    if app is None:
        reasons.append("You have not applied for this exam.")
    else:
        if app["status"] != "approved":
            reasons.append("Your exam application has not been approved yet.")
        if not app["fee_paid"]:
            reasons.append("Exam fee payment is pending.")
    # ID doc verified?
    id_docs = [
        d
        for d in DOCUMENTS
        if d["student_id"] == sid and d["doc_type"] == "ID Proof"
    ]
    if not any(d["status"] == "verified" for d in id_docs):
        reasons.append("Government ID document must be verified.")
    # Course fee status
    course_fees = [
        f
        for f in FEES
        if f["student_id"] == sid and f["course_id"] == exam["course_id"]
    ]
    if not any(f["status"] == "paid" for f in course_fees):
        reasons.append("Course fee for this program is not marked as paid.")
    return (len(reasons) == 0, reasons)


def update_fee_status(
    fee_id: int, new_status: str, updater: int
) -> tuple[bool, str]:
    for f in FEES:
        if f["id"] == fee_id:
            f["status"] = new_status
            f["updated_at"] = _now_str()
            f["updated_by"] = updater
            return True, "Fee status updated."
    return False, "Fee record not found."


def verify_document(
    doc_id: int, new_status: str, note: str
) -> tuple[bool, str]:
    for d in DOCUMENTS:
        if d["id"] == doc_id:
            d["status"] = new_status
            d["reviewer_note"] = note
            return True, f"Document marked {new_status}."
    return False, "Document not found."


def recommend_exam_mode(app_id: int, mode: str) -> tuple[bool, str]:
    for a in EXAM_APPLICATIONS:
        if a["id"] == app_id:
            a["institute_recommended_mode"] = mode
            a["status"] = "forwarded"
            return (
                True,
                "Exam mode recommendation saved and application forwarded.",
            )
    return False, "Application not found."


def mark_attendance(
    course_id: int, student_id: int, date: str, status: str, faculty_id: int
) -> tuple[bool, str]:
    for a in ATTENDANCE:
        if (
            a["course_id"] == course_id
            and a["student_id"] == student_id
            and a["date"] == date
        ):
            a["status"] = status
            a["marked_by"] = faculty_id
            return True, "Attendance updated."
    _counters["attendance"] += 1
    ATTENDANCE.append(
        {
            "id": _counters["attendance"],
            "course_id": course_id,
            "student_id": student_id,
            "date": date,
            "status": status,
            "marked_by": faculty_id,
        }
    )
    return True, "Attendance recorded."


def add_assessment(
    course_id: int,
    student_id: int,
    title: str,
    marks: float,
    max_marks: float,
    remarks: str,
    faculty_id: int,
) -> tuple[bool, str]:
    if max_marks <= 0:
        return False, "Max marks must be greater than zero."
    if marks < 0 or marks > max_marks:
        return False, f"Marks must be between 0 and {max_marks:.0f}."
    _counters["assessment"] += 1
    ASSESSMENTS.append(
        {
            "id": _counters["assessment"],
            "course_id": course_id,
            "student_id": student_id,
            "title": title,
            "marks": marks,
            "max_marks": max_marks,
            "remarks": remarks,
            "graded_by": faculty_id,
            "graded_at": _now_str(),
        }
    )
    return True, "Assessment recorded."


def add_practical(
    course_id: int,
    student_id: int,
    title: str,
    grade: str,
    remarks: str,
    faculty_id: int,
) -> tuple[bool, str]:
    if not grade:
        return False, "Grade is required."
    _counters["practical"] += 1
    PRACTICALS.append(
        {
            "id": _counters["practical"],
            "course_id": course_id,
            "student_id": student_id,
            "title": title,
            "grade": grade,
            "remarks": remarks,
            "graded_by": faculty_id,
            "graded_at": _now_str(),
        }
    )
    return True, "Practical evaluation recorded."


def all_students() -> list[UserRec]:
    return [u for u in USERS if u["role"] == "student"]


def compute_grade(marks: float, max_marks: float) -> tuple[str, bool]:
    if max_marks <= 0:
        return "F", False
    pct = (marks / max_marks) * 100.0
    if pct >= 90:
        return "A+", True
    if pct >= 80:
        return "A", True
    if pct >= 70:
        return "B+", True
    if pct >= 60:
        return "B", True
    if pct >= 50:
        return "C", True
    if pct >= 40:
        return "D", True
    return "F", False


def approve_application(
    app_id: int, actor_id: int, note: str
) -> tuple[bool, str]:
    for a in EXAM_APPLICATIONS:
        if a["id"] == app_id:
            if a["status"] not in ("forwarded", "pending"):
                return False, f"Application is already {a['status']}."
            a["status"] = "approved"
            a["fee_paid"] = True
            push_notification(
                a["student_id"],
                "Exam application approved",
                f"Your application has been approved. {note}".strip(),
            )
            add_audit_log(
                actor_id,
                "university",
                "approve_application",
                "exam_application",
                app_id,
                note or "Approved",
            )
            return True, "Application approved."
    return False, "Application not found."


def reject_application(
    app_id: int, actor_id: int, note: str
) -> tuple[bool, str]:
    for a in EXAM_APPLICATIONS:
        if a["id"] == app_id:
            if a["status"] == "rejected":
                return False, "Application already rejected."
            a["status"] = "rejected"
            push_notification(
                a["student_id"],
                "Exam application rejected",
                f"Reason: {note}" if note else "Your application was rejected.",
            )
            add_audit_log(
                actor_id,
                "university",
                "reject_application",
                "exam_application",
                app_id,
                note or "Rejected",
            )
            return True, "Application rejected."
    return False, "Application not found."


def declare_result(
    exam_id: int,
    student_id: int,
    marks: float,
    actor_id: int,
) -> tuple[bool, str]:
    exam = find_exam(exam_id)
    if exam is None:
        return False, "Exam not found."
    if marks < 0 or marks > exam["max_marks"]:
        return False, f"Marks must be between 0 and {exam['max_marks']}."
    grade, passed = compute_grade(float(marks), float(exam["max_marks"]))
    for r in RESULTS:
        if r["exam_id"] == exam_id and r["student_id"] == student_id:
            r["marks"] = marks
            r["max_marks"] = exam["max_marks"]
            r["grade"] = grade
            r["declared_at"] = _now_str()
            r["declared"] = True
            push_notification(
                student_id,
                "Result declared",
                f"{exam['title']}: {marks:.0f}/{exam['max_marks']} · Grade {grade}",
            )
            add_audit_log(
                actor_id,
                "university",
                "declare_result",
                "exam",
                exam_id,
                f"Student {student_id}: {marks}/{exam['max_marks']} ({grade})",
            )
            return True, f"Result declared. Grade {grade}."
    _counters["result"] += 1
    RESULTS.append(
        {
            "id": _counters["result"],
            "exam_id": exam_id,
            "student_id": student_id,
            "marks": marks,
            "max_marks": exam["max_marks"],
            "grade": grade,
            "declared_at": _now_str(),
            "declared": True,
        }
    )
    push_notification(
        student_id,
        "Result declared",
        f"{exam['title']}: {marks:.0f}/{exam['max_marks']} · Grade {grade}",
    )
    add_audit_log(
        actor_id,
        "university",
        "declare_result",
        "exam",
        exam_id,
        f"Student {student_id}: {marks}/{exam['max_marks']} ({grade})",
    )
    if passed:
        # Auto-create pending certificate
        _counters["certificate"] += 1
        course = find_course(exam["course_id"])
        CERTIFICATES.append(
            {
                "id": _counters["certificate"],
                "student_id": student_id,
                "course_id": exam["course_id"],
                "title": (course["title"] if course else "Course")
                + " - Completion",
                "issued_at": _now_str(),
                "status": "pending",
            }
        )
    return True, f"Result declared. Grade {grade}."


def approve_certificate(
    cert_id: int, actor_id: int, note: str
) -> tuple[bool, str]:
    for c in CERTIFICATES:
        if c["id"] == cert_id:
            if c["status"] == "issued":
                return False, "Certificate already issued."
            c["status"] = "issued"
            c["issued_at"] = _now_str()
            push_notification(
                c["student_id"],
                "Certificate issued",
                f"Your certificate '{c['title']}' has been approved.",
            )
            add_audit_log(
                actor_id,
                "university",
                "approve_certificate",
                "certificate",
                cert_id,
                note or "Approved",
            )
            return True, "Certificate approved and issued."
    return False, "Certificate not found."


def reject_certificate(
    cert_id: int, actor_id: int, note: str
) -> tuple[bool, str]:
    for c in CERTIFICATES:
        if c["id"] == cert_id:
            c["status"] = "rejected"
            push_notification(
                c["student_id"],
                "Certificate rejected",
                f"Reason: {note}" if note else "Certificate rejected.",
            )
            add_audit_log(
                actor_id,
                "university",
                "reject_certificate",
                "certificate",
                cert_id,
                note or "Rejected",
            )
            return True, "Certificate rejected."
    return False, "Certificate not found."


def admin_create_user(
    email: str,
    password: str,
    full_name: str,
    role: str,
    actor_id: int,
) -> tuple[bool, str]:
    if not email or not password or not full_name:
        return False, "All fields are required."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if role not in ROLES:
        return False, "Invalid role."
    if find_user(email) is not None:
        return False, "Email already exists."
    user = register_user(email, password, full_name, role)
    if user is None:
        return False, "Could not create user."
    add_audit_log(
        actor_id,
        "super_admin",
        "create_user",
        "user",
        user["id"],
        f"Created {role} account for {email}",
    )
    return True, f"User created: {email}"


def toggle_user_active(uid: int, actor_id: int) -> tuple[bool, str]:
    for u in USERS:
        if u["id"] == uid:
            u["is_active"] = not u["is_active"]
            state = "activated" if u["is_active"] else "deactivated"
            add_audit_log(
                actor_id,
                "super_admin",
                "toggle_user_active",
                "user",
                uid,
                f"User {state}",
            )
            return True, f"User {state}."
    return False, "User not found."


def mark_contact_read(cid: int, is_read: bool) -> None:
    for m in CONTACT_MESSAGES:
        if m["id"] == cid:
            m["is_read"] = is_read
            return


def mark_contact_responded(cid: int, is_responded: bool) -> None:
    for m in CONTACT_MESSAGES:
        if m["id"] == cid:
            m["is_responded"] = is_responded
            if is_responded:
                m["is_read"] = True
            return


def get_certificate(cid: int) -> CertificateRec | None:
    for c in CERTIFICATES:
        if c["id"] == cid:
            return c
    return None


# Seed some initial audit logs and pending certificate approvals
add_audit_log(5, "super_admin", "system_init", "system", 0, "Platform seeded.")
if CERTIFICATES:
    add_audit_log(
        4,
        "university",
        "approve_certificate",
        "certificate",
        CERTIFICATES[0]["id"],
        "Auto-issued for demo",
    )

# Add an extra pending certificate for demo
if COURSES and STUDENT_PROFILES:
    _counters["certificate"] += 1
    CERTIFICATES.append(
        {
            "id": _counters["certificate"],
            "student_id": STUDENT_PROFILES[0]["user_id"],
            "course_id": COURSES[1]["id"],
            "title": COURSES[1]["title"] + " - Completion",
            "issued_at": _now_str(),
            "status": "pending",
        }
    )
