from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            send_mail(
                subject="Добро пожаловать!",
                message=f"Здравствуйте, {user.email}! Добро пожаловать на наш сайт.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})
