"""
Content-type validating middleware.
For each endpoint it checks the content-type of the request
and returns 400 if it is not as registered in the __content_type_map.
"""

from werkzeug.wrappers import Request, Response


class ContentTypeMiddleware(object):
    Logger = None

    __content_type_map = {
        "/cars": "application/json",
        "/journey": "application/json",
        "/dropoff": "application/x-www-form-urlencoded",
        "/locate": "application/x-www-form-urlencoded",
    }

    def __init__(self, app):
        self.app = app
        self.wsgi_app = app.wsgi_app

    def __call__(self, environ, start_response):
        request = Request(environ)
        self.app.logger.info(
            f"Request received from {request.remote_addr} to {request.path}"
        )

        if request.path in ContentTypeMiddleware.__content_type_map:
            self.app.logger.debug(
                f"request content-type: {request.content_type}, expected: {ContentTypeMiddleware.__content_type_map[request.path]}"
            )
            if (
                request.content_type
                not in ContentTypeMiddleware.__content_type_map[request.path]
            ):
                failed_resp = Response(status=400)
                return failed_resp(environ, start_response)

        return self.wsgi_app(environ, start_response)
