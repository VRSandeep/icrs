from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.context_processors import csrf
from django.shortcuts import render_to_response

from django.contrib.admin.views.decorators import staff_member_required


def populate_context(request):
    context = {}
    if context:
        context.clear()
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
def interviewer(request, *args, **kwargs):
    from interview.views import get_previous_candidates, search_candidates
    context = populate_context(request)

    if request.GET.get('search', ''):
        context['candidates'] = search_candidates(request.GET['search'], request)
    else:
        context['candidates'] = get_previous_candidates(request)

    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(context['candidates'])
    return render_to_response('website/interviewer.html', context)


@login_required
@user_passes_test(lambda u: not u.is_staff and not u.is_superuser)
def candidate(request):
    context = populate_context(request)
    return render_to_response('website/candidate.html', context)
