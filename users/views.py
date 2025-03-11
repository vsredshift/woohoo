from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created. You can now login."
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if not hasattr(request.user, "profile"):
        Profile.objects.create(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
            user=request.user,
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile, user=request.user)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "users/profile.html", context)


class StaffListView(ListView):
    model = User
    template_name = "users/staff_list.html"
    context_object_name = "staff_members"

    def get_queryset(self):
        return User.objects.filter(is_staff=True).select_related("profile")
    