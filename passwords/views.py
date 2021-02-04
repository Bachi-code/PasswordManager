from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from passwords.forms import CustomUserCreationForm, PasswordCreate
from passwords.models import PasswordEntry
from pwned_passwords_django.api import pwned_password
import string
import secrets


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, "Account created successfully.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/register.html", {"form": form})


@login_required
def password_create(request):
    if request.method == "POST":
        form = PasswordCreate(request.POST, user=request.user)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.owner_password = request.user
            entry.save()
            messages.success(request, "Password saved successfully.")
            return redirect('home')
    else:
        form = PasswordCreate()
    return render(request, "password/password_create.html", {"form": form})


@login_required
def password_list(request):
    if request.method == 'POST' and request.is_ajax():
        user = request.user
        pk = request.POST.get('password_id')
        check = request.POST.get('check_p')
        password = PasswordEntry.objects.get(pk=pk, owner_password=user)
        test = password.decrypt_password()
        if check == "True":
            count = pwned_password(test)
            if count is None:
                return JsonResponse({'password': 0})
            else:
                return JsonResponse({'password': count})
        else:
            return JsonResponse({'password': test})
    user = request.user
    passwords = PasswordEntry.objects.filter(owner_password=user)
    return render(request, "password/password_list.html", {"passwords": passwords})


@login_required
def password_delete(request, pk):
    user = request.user
    password = get_object_or_404(PasswordEntry, id=pk, owner_password=user)
    if request.method == 'POST':
        password.delete()
        messages.success(request, "Password deleted successfully.")
        return redirect('password_list')
    return render(request, "password/password_delete.html", {"password": password})


def generator(request):
    if request.is_ajax():
        charset = ""
        basicsymbols = ';:><.,?/\"\'[{]}\|+=_-)(*&^%$#@!`~'
        length = request.GET.get('length')
        if isinstance(length, str):
            length = int(length)
        else:
            length = 10

        if request.GET.get('uppercase') == 'true':
            charset += string.ascii_uppercase
            uppercases_included = True
        else:
            uppercases_included = False

        if request.GET.get('symbols') == 'true':
            charset += basicsymbols
            basicsymbols_included = True
        else:
            basicsymbols_included = False

        if request.GET.get('numbers') == 'true':
            charset += string.digits
            digits_included = True
        else:
            digits_included = False

        if request.GET.get('lowercase') == 'true':
            charset += string.ascii_lowercase
            lowercases_included = True
        else:
            lowercases_included = False

        while True:
            password = ""
            lowercase_showed_up = False
            uppercase_showed_up = False
            basicsymbol_showed_up = False
            digit_showed_up = False
            char = ""
            for index in range(length):
                if charset == "":
                    return JsonResponse({"error": ""}, status=400)
                else:
                    char = secrets.choice(charset)
                password += char
                if request.GET.get('forceall') == 'true':
                    if char in string.ascii_uppercase:
                        uppercase_showed_up = True
                    if char in string.digits:
                        digit_showed_up = True
                    if char in string.ascii_lowercase:
                        lowercase_showed_up = True
                    if char in basicsymbols:
                        basicsymbol_showed_up = True

            if request.GET.get('forceall') == 'true':
                if ((not (lowercases_included) or lowercase_showed_up) and (
                        not (uppercases_included) or uppercase_showed_up) and (
                        not (digits_included) or digit_showed_up) and (
                        not (basicsymbols_included) or basicsymbol_showed_up)):
                    return JsonResponse({'the_pass': password})
            else:
                return JsonResponse({'the_pass': password})

    return render(request, 'generator.html', {'range': range(8, 31)})
