import os
import secrets
import urllib.parse
import logging
import reflex as rx
import httpx
from app.data.seed import link_or_create_oauth_user
from app.states.auth_state import AuthState, ROLE_ROUTES


def _base_url() -> str:
    return os.getenv("APP_BASE_URL", "http://localhost:3000").rstrip("/")


def google_configured() -> bool:
    return bool(
        os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET")
    )


def github_configured() -> bool:
    return bool(
        os.getenv("GITHUB_CLIENT_ID") and os.getenv("GITHUB_CLIENT_SECRET")
    )


class OAuthState(rx.State):
    error: str = ""
    status: str = ""
    pending_state: str = ""
    pending_provider: str = ""

    @rx.event
    def start_google(self):
        if not google_configured():
            self.error = "Google sign-in is not configured on this server."
            return rx.toast(self.error, duration=4000, close_button=True)
        state = secrets.token_urlsafe(16)
        self.pending_state = state
        self.pending_provider = "google"
        params = {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "redirect_uri": f"{_base_url()}/auth/callback/google",
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "online",
            "prompt": "select_account",
        }
        url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            + urllib.parse.urlencode(params)
        )
        return rx.redirect(url, external=True)

    @rx.event
    def start_github(self):
        if not github_configured():
            self.error = "GitHub sign-in is not configured on this server."
            return rx.toast(self.error, duration=4000, close_button=True)
        state = secrets.token_urlsafe(16)
        self.pending_state = state
        self.pending_provider = "github"
        params = {
            "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
            "redirect_uri": f"{_base_url()}/auth/callback/github",
            "scope": "read:user user:email",
            "state": state,
            "allow_signup": "true",
        }
        url = (
            "https://github.com/login/oauth/authorize?"
            + urllib.parse.urlencode(params)
        )
        return rx.redirect(url, external=True)

    async def _finalize(self, email: str, name: str, provider: str, uid: str):
        user = link_or_create_oauth_user(provider, uid, email, name)
        if user is None:
            self.error = (
                "Could not complete sign-in — missing email from provider."
            )
            return rx.redirect("/login")
        if not user["is_active"]:
            self.error = (
                "This account is inactive. Please contact administration."
            )
            return rx.redirect("/login")
        auth = await self.get_state(AuthState)
        auth.user_id = user["id"]
        auth.user_email = user["email"]
        auth.user_name = user["full_name"]
        auth.user_role = user["role"]
        auth.error = ""
        self.status = f"Signed in via {provider.title()}"
        self.error = ""
        return rx.redirect(ROLE_ROUTES.get(user["role"], "/"))

    @rx.event
    async def handle_google_callback(self):
        try:
            params = self.router.page.params
            if params.get("error"):
                self.error = f"Google sign-in cancelled: {params.get('error')}"
                return rx.redirect("/login")
            code = params.get("code", "")
            if not code:
                self.error = "Google sign-in failed: missing code."
                return rx.redirect("/login")
            if not google_configured():
                self.error = "Google sign-in not configured."
                return rx.redirect("/login")
            async with httpx.AsyncClient(timeout=15) as client:
                token_resp = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "code": code,
                        "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
                        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
                        "redirect_uri": f"{_base_url()}/auth/callback/google",
                        "grant_type": "authorization_code",
                    },
                )
                if token_resp.status_code != 200:
                    self.error = "Google sign-in failed: token exchange error."
                    return rx.redirect("/login")
                access_token = token_resp.json().get("access_token", "")
                if not access_token:
                    self.error = "Google sign-in failed: no access token."
                    return rx.redirect("/login")
                userinfo = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                if userinfo.status_code != 200:
                    self.error = "Google sign-in failed: userinfo error."
                    return rx.redirect("/login")
                data = userinfo.json()
            email = (data.get("email") or "").strip()
            name = data.get("name") or email.split("@")[0]
            uid = str(data.get("id", email))
            return await OAuthState._finalize(email, name, "google", uid)
        except Exception as e:
            logging.exception(f"Google OAuth error: {e}")
            self.error = "Google sign-in failed unexpectedly."
            return rx.redirect("/login")

    @rx.event
    async def handle_github_callback(self):
        try:
            params = self.router.page.params
            if params.get("error"):
                self.error = f"GitHub sign-in cancelled: {params.get('error')}"
                return rx.redirect("/login")
            code = params.get("code", "")
            if not code:
                self.error = "GitHub sign-in failed: missing code."
                return rx.redirect("/login")
            if not github_configured():
                self.error = "GitHub sign-in not configured."
                return rx.redirect("/login")
            async with httpx.AsyncClient(timeout=15) as client:
                token_resp = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
                        "client_secret": os.getenv("GITHUB_CLIENT_SECRET", ""),
                        "code": code,
                        "redirect_uri": f"{_base_url()}/auth/callback/github",
                    },
                    headers={"Accept": "application/json"},
                )
                if token_resp.status_code != 200:
                    self.error = "GitHub sign-in failed: token exchange."
                    return rx.redirect("/login")
                access_token = token_resp.json().get("access_token", "")
                if not access_token:
                    self.error = "GitHub sign-in failed: no access token."
                    return rx.redirect("/login")
                user_resp = await client.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/vnd.github+json",
                    },
                )
                if user_resp.status_code != 200:
                    self.error = "GitHub sign-in failed: user fetch."
                    return rx.redirect("/login")
                user_data = user_resp.json()
                email = user_data.get("email") or ""
                if not email:
                    emails_resp = await client.get(
                        "https://api.github.com/user/emails",
                        headers={
                            "Authorization": f"Bearer {access_token}",
                            "Accept": "application/vnd.github+json",
                        },
                    )
                    if emails_resp.status_code == 200:
                        for e in emails_resp.json():
                            if e.get("primary") and e.get("verified"):
                                email = e.get("email", "")
                                break
                        if not email:
                            for e in emails_resp.json():
                                if e.get("email"):
                                    email = e.get("email")
                                    break
            if not email:
                self.error = (
                    "GitHub did not return a verified email. "
                    "Please make your email public or use another sign-in method."
                )
                return rx.redirect("/login")
            name = user_data.get("name") or user_data.get("login") or email
            uid = str(user_data.get("id", email))
            return await OAuthState._finalize(email, name, "github", uid)
        except Exception as e:
            logging.exception(f"GitHub OAuth error: {e}")
            self.error = "GitHub sign-in failed unexpectedly."
            return rx.redirect("/login")

    @rx.var
    def google_available(self) -> bool:
        return google_configured()

    @rx.var
    def github_available(self) -> bool:
        return github_configured()
