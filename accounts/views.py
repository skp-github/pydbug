from django.shortcuts import render, redirect
from django.views.generic import RedirectView, TemplateView
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from accounts.models import Profile as profile
# Create your views here.



class Profile(RedirectView):
    """

    """
    permanent = False
    query_string = True
    pattern_name = 'redirections'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            print('m here')
            return reverse_lazy('login')
        return reverse_lazy('list_project')
        # elif self.request.user.profile.user_type == 'TAG':
        #     return reverse_lazy('pending_panel')
        # elif self.request.user.profile.branch_user:
        #     return reverse_lazy('information_infofeed_panel')
        # elif self.request.user.profile.user_type in ['UNIT', 'ZONE']:
        #     return reverse_lazy('information_list_view', kwargs={'status': 'pending'})
        # elif self.request.user.profile.user_type in ['HS', 'STATE']:
        #     return reverse_lazy('information_list_view', kwargs={'status': 'search'})
        # elif self.request.user.profile.user_type in ['FIELD']:
        #     return reverse_lazy('information_list_view', kwargs={'status': 'sentbyme'})
        # return reverse_lazy('handler', args=['403'])


def register_superuser(request):
    # TODO: register user
    if request.method == 'GET':
        return render(request, 'registration/register.html', {})
    else:
        # TODO: check errors and stuff
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            user_obj = User.objects.get(username=username)
            user_obj.email = request.POST.get('email')
            user_obj.first_name = request.POST.get('firstname')
            user_obj.last_name = request.POST.get('lastname')
            user_obj.is_active = True
            user_obj.save()
            profile_obj = profile(user=user_obj, access_type=0)
            profile_obj.save()
            return redirect('list_project')
        else:
            return render(request, 'registration/register.html', {'form': form})



class HandlerPage(TemplateView):
    """

    """

    def get_template_names(self):
        code = self.kwargs.get('code', '404')
        if code not in ['404', '403', '401', '500']:
            code = '404'
        return ["registration/{}.html".format(code)]


def return_404(request):
    response = render( request,
        'registration/404.html',
        context_instance=RequestContext(request)
        )

    response.status_code = 404

    return response