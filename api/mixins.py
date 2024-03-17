from utils.responses import Response


class HandleExceptionMixin(object):

    def handle_exception(self, exc):
        message = None
        error = str(exc)
        if getattr(exc, 'detail', None):
            error = exc.detail
            if isinstance(exc.detail, dict):
                message = exc.detail.get('message')
        elif getattr(exc, 'message', None):
            error = exc.message
        return Response(error=error, status=getattr(exc, 'status_code', 400), message=message, success=False)
