## Phase 1: Foundation, Public Website, Authentication, and Seeded Data ✅
- [x] Establish a cohesive ROAN dark glassmorphism design direction: deep navy background, warm gold accents, cream text, responsive mobile-first layouts, animated cards, and shared navigation.
- [x] Build the public marketing website pages with branch showcase, live Guitar Academy course content, coming-soon branches, testimonials, contact form persistence, footer, mobile navigation, and styled 404 experience.
- [x] Create the database-backed core platform data model, seed realistic demo data for all roles, users, courses, students, faculty, exams, fees, documents, results, notifications, and audit activity.
- [x] Implement email/password authentication with hashed credentials, role-based login routing, registration flow, logout, inactive-user handling, and forgot-password stub.
- [x] Enforce server-side role authorization for every protected portal route with redirect or not-authorized handling.

## Phase 2: Student, Faculty, and Institute Portals ✅
- [x] Build the shared protected portal shell with persistent sidebar, topbar, role-specific navigation, avatar/name display, logout controls, responsive behavior, loading states, and empty states.
- [x] Implement the Student portal dashboards and workflows for course enrollment, exam applications, results, documents, notifications, profile editing, certificates, and admit-card eligibility messaging.
- [x] Implement the Faculty portal dashboards and workflows for attendance, assessments, practical evaluations, student directory, and reporting.
- [x] Implement the Institute portal dashboards and workflows for application verification, document review, fee status updates, exam-mode recommendations, and forwarded queue.
- [x] Ensure all portal actions persist to the database, show clear validation errors, produce success/error feedback, and refresh displayed data immediately.

## Phase 3: University, Super Admin, PDFs, Analytics, Export, and Final Workflows ✅
- [x] Implement the University portal dashboards and workflows for application approvals, result declaration, certificate approvals, and approval audit trails.
- [x] Implement the Super Admin portal dashboards and workflows for user management, contact messages, audit logs, analytics charts, and backup export.
- [x] Generate real PDFs for certificates and admit cards with server-side eligibility and approval validation before download.
- [x] Complete real chart-based analytics for students, applications, enrollments, results, fees, and pipeline activity.
- [x] Finalize mobile responsiveness, form validation, empty/loading states, toast feedback, audit logging coverage, and cross-role authorization consistency.

## Phase 4: OAuth, Visual Depth, and Remaining Polish ✅
- [x] Add additive Google and GitHub sign-in options with default student onboarding, provider linking, failure handling, and existing role-based redirects.
- [x] Add layered hero depth, subtle animated glow backgrounds, and responsive visual effects for public and authentication experiences.
- [x] Add tactile hover depth to branch cards, portal metrics, course cards, and certificate/admit-card surfaces while keeping mobile behavior performant.
- [x] Complete a cross-page polish pass for links, empty states, loading states, toasts, PDFs, responsive navigation, forms, tables, and route protection.