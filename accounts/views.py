from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import login as auth_login
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .forms import UserRegisterSerializer


class Register(generics.GenericAPIView):
    """
    Creates User Account

    Returns: SESSION cookie on success and 201 status; Errors and 4xx status code on failure
    """

    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def post_register(self):
        auth_login(self.request, self.user)

    def get_response(self):
        return Response(status=status.HTTP_201_CREATED)

    def get_error_response(self):
        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            return self.get_error_response()

        self.user = self.serializer.save()
        self.post_register()
        return self.get_response()


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_staff(request):
    authentication_form = AdminAuthenticationForm
    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    return HttpResponse(status=405)
