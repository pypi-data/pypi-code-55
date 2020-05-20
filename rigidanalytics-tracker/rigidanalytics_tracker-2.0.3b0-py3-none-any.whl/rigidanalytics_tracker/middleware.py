from .django import Tracker


class Analytics(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.intercepted_data = {}
        self.tracker = Tracker()

    def __call__(self, request):
        if self.tracker.is_disabled():
            return self.get_response(request)

        self.tracker.start(request)

        response = self.get_response(request)

        self.tracker.stop(response)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.tracker.set_intercepted_data('view_name', view_func.__name__)
