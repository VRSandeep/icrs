from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse

from .forms import CandidateRegistrationForm


def register_candidate(request):
    form = CandidateRegistrationForm(request.POST)     # create form object
    context = {}
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('register_candidate'))
        context['form'] = form
    else:
        context['form'] = CandidateRegistrationForm()
    context.update(csrf(request))

    return render(request, 'accounts/register.html', context)

