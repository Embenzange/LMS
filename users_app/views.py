from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from curriculum.models import Standard
from users_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from .models import user_profile 
from users_app.models import Contact
# Create your views here.
def index(request):
    return render(request, 'base.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please input correct username and password")
        
    else:
        return render(request, 'users_app/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == "POST":
        userform = UserForm(data=request.POST)
        profileform = UserProfileInfoForm(data=request.POST)

        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.save()

            profile = profileform.save(commit=False)
            profile.user = user
            profile.save()

            registered=True
        else:
            print(userform.errors, profileform.errors)

    else:
        userform = UserForm()
        profileform = UserProfileInfoForm()

    return render(request, 'users_app/registration.html',
                  {'registered':registered,
                   'userform':userform,
                   'profileform':profileform})
    

class HomeView(TemplateView):
    template_name = 'users_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = user_profile.objects.filter(user_type='teacher')
        context['standards'] = standards
        context['teachers'] = teachers
        return context

class ContactView(CreateView):
    model = Contact
    fields = '__all__'
    template_name = 'users_app/contact.html'
