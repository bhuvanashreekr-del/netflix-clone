import time
import logging
from .models import RequestLog

logger = logging.getLogger('myapp.requests')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        # Process request
        response = self.get_response(request)
        
        duration_ms = (time.time() - start_time) * 1000.0

        # Don't log static files to avoid cluttering DB
        path = request.path
        if not path.startswith('/static/') and not path.startswith('/favicon.ico'):
            try:
                # Get client IP
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0].strip()
                else:
                    ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

                ua = request.META.get('HTTP_USER_AGENT', '')[:290]

                RequestLog.objects.create(
                    path=path[:290],
                    method=request.method,
                    status_code=response.status_code,
                    duration_ms=round(duration_ms, 2),
                    ip_address=ip,
                    user_agent=ua
                )
                logger.info(f'{request.method} {path} -> {response.status_code} ({duration_ms:.1f}ms)')
            except Exception as e:
                logger.error(f'Failed to log request: {e}')

        # Add latency header
        response['X-Response-Time'] = f'{duration_ms:.2f}ms'
        return response
