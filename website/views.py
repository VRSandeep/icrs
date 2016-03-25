from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required


def populate_context(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        context['user'] = request.user
        context['authenticated'] = request.user.is_authenticated()
    else:
        context.pop('user', None)
    return context


def home(request):
    context = populate_context(request)
    return render_to_response('website/index.html', context)


@staff_member_required(login_url=settings.LOGIN_URL)
def interviewer(request):
    from interview.views import get_previous_candidates
    context = populate_context(request)
    User = get_user_model()
    context['candidates'] = get_previous_candidates(request)
    # print context['candidates']

    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(context['candidates'])

    return render_to_response('website/interviewer.html', context)


@login_required
@user_passes_test(lambda u: not u.is_staff and not u.is_superuser)
def candidate(request):
    return render_to_response('website/candidate.html', populate_context(request))
