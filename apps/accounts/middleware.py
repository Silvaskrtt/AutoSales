import re
from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    """Middleware that requires a user to be authenticated to view any page.

    Exemptions can be configured via `LOGIN_EXEMPT_URLS` in settings (list of
    regex strings). By default, the middleware exempts:
      - the login/logout/account URLs (`/accounts/`)
      - the admin site (`/admin/`)
      - static and media files
    """

    def __init__(self, get_response):
        self.get_response = get_response
        exempt = getattr(settings, 'LOGIN_EXEMPT_URLS', None)
        if exempt is None:
            exempt = [r'^/accounts/', r'^/admin/', r'^/static/', r'^/media/', r'^/favicon.ico$']
        self.exempt_urls = [re.compile(expr) for expr in exempt]

    def __call__(self, request):
        # If user is authenticated or path is exempt, continue
        if request.user.is_authenticated:
            return self.get_response(request)

        path = request.path_info
        for rx in self.exempt_urls:
            if rx.search(path):
                return self.get_response(request)

        # Redirect to login with next param
        login_url = settings.LOGIN_URL or '/accounts/login/'
        return redirect(f"{login_url}?next={request.path}")
