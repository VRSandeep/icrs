from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CandidateRegistrationForm(UserCreationForm):

    def save(self, commit=True):
        user = super(CandidateRegistrationForm, self).save(commit=True)
        from django.contrib.auth.models import Group
        g, _ = Group.objects.get_or_create(name='candidates')
        if commit:
            user.groups.add(g)
            user.save()
            user = authenticate(username=user.username, password=self.cleaned_data['password1'])
        return user
