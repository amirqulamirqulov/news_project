from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from .models import Profile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from news_app.models import Comment, Category

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Mufaqqiyatli login amalga oshirildi!')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas!')
            else:
                return HttpResponse('Username yoki passwordda xatolik bor.')
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


@login_required()
def dashbord_user(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    context = {
        "user": user,
        "profile": profile
    }
    return render(request, 'pages/user_profile.html', context)


def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('login')
    else:
        form = UserRegisterForm()
        context = {
            "form": form
        }
        return render(request, 'registration/user_register.html', context)


class RegistrationView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/user_register.html"


@login_required()
def update_user(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        profile_form = ProfileUpdateForm(instance=request.user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'pages/update_profile.html', context)


class UpdateUser(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'pages/update_profile.html', context)

    def post(self, request):
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        profile_form = ProfileUpdateForm(instance=request.user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    if request.method == 'GET':

        admin_list = User.objects.filter(is_superuser=True)
        categories = Category.objects.all()
        comment_list = Comment.objects.all()
        context = {
            "admin_list": admin_list,
            'comment_list': comment_list,
            'category': categories,
        }
        return render(request, "pages/admin_page.html", context)
    else:
        comment_list = Comment.objects.all()
        list_active = [x for x in request.POST]
        for y in comment_list:
            if str(y.id) in list_active:
                y.active = True
            else:
                y.active = False
            y.save()

        comment_list = Comment.objects.all()
        admin_list = User.objects.filter(is_superuser=True)
        categories = Category.objects.all()
        context = {
            "admin_list": admin_list,
            'comment_list': comment_list,
            'category': categories,
        }
        return render(request, "pages/admin_page.html", context)

