from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, View, DeleteView
from passwords.forms import CustomUserCreationForm, PasswordCreate
from passwords.models import PasswordEntry
from pwned_passwords_django.api import pwned_password
import string
import secrets


class HomeView(TemplateView):
    template_name = "home.html"


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "auth/register.html"
    success_url = reverse_lazy("home")
    form_class = CustomUserCreationForm
    success_message = "Account created successfully."


class PasswordCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "password/password_create.html"
    success_url = reverse_lazy("password_list")
    form_class = PasswordCreate
    success_message = "Password saved successfully."

    def form_valid(self, form):
        form.instance.owner_password = self.request.user
        return super().form_valid(form)


class PasswordListView(LoginRequiredMixin, TemplateView):
    template_name = "password/password_list.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordListView, self).get_context_data(**kwargs)
        context["passwords"] = PasswordEntry.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        pk = self.request.POST.get('password_id')
        check = self.request.POST.get('check_p')
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


class PasswordDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "password/password_delete.html"
    model = PasswordEntry
    success_url = reverse_lazy("password_list")
    success_message = "Password deleted successfully."

    def get_object(self, queryset=None):
        obj = super(PasswordDeleteView, self).get_object()
        if not obj.owner_password == self.request.user:
            raise Http404
        return obj


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
