import requests
from django.contrib.auth import logout
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.utils import translation
from django.conf import settings
from django.shortcuts import redirect


class LogoutView(RedirectView):
    url = reverse_lazy('dashboard:combined-list')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)



def change_language(request, lang_code):
    # Check if the language code is in the available languages
    supported_languages = [lang_code for lang_code, _ in settings.LANGUAGES]

    if lang_code in supported_languages:
        # Activate the selected language
        translation.activate(lang_code)

        # Store the language in the session or cookie (depending on your setup)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code  # Store in session

        # Set the language in the response cookie (if you want cookie-based language persistence)
        response = redirect(request.GET.get('next', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return response

    return redirect('/')
