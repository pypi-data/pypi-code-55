import logging

logger = logging.getLogger(__name__)


class MusesPagesViews:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        logger.info("Enter in MusesPagesViews")

        if request.user.is_authenticated and request.method == "GET":
            request.user.page_views_counter += 1
            request.user.save()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        logger.info("Exit from MusesPagesViews")

        return response
