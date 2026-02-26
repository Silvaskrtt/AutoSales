from .threadlocals import set_current_user, set_current_ip, clear


class AuditMiddleware:
    """Middleware that stores request.user and client IP in thread-local storage

    Signals use these values to attribute audit records to the current request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user = getattr(request, 'user', None)
            set_current_user(user if user and user.is_authenticated else None)
            # get client IP (X-Forwarded-For fallback)
            xff = request.META.get('HTTP_X_FORWARDED_FOR')
            if xff:
                ip = xff.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            set_current_ip(ip)
            response = self.get_response(request)
            return response
        finally:
            clear()
