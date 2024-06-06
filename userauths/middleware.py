from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path in [reverse('userauths:sign-in'), reverse('userauths:sign-up')]:
                return redirect('core:feed')  # hoặc tên URL của trang chủ của bạn

        response = self.get_response(request)
        return response
