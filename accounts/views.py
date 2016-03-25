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

from .forms import CandidateRegistrationForm


def register_candidate(request):
    context = {}
    if request.POST:
        form = CandidateRegistrationForm(request.POST)     # create form object
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('register_candidate'))
        context['form'] = form
    else:
        context['form'] = CandidateRegistrationForm()
    context.update(csrf(request))

    return render(request, 'accounts/register.html', context)


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
