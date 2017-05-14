from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.generic import FormView
from django.conf import settings

from .forms import ContactForm


# Create your views here.

class ContactFormView(FormView):
    template_name = "contact.html"
    form_class = ContactForm


def send_message(request):
    if request.method == 'POST':
        try:
            fullname = request.POST.get("fullname")
            email = request.POST.get("email")
            message = request.POST.get("message")
        except:
            fullname = None
            email = None
            message = None

        response_data = {
            "is_success": False,
        }

        if fullname is not None:
            send_mail("Contact from " + fullname + ", " + email, message,
                      settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            response_data["is_success"] = True
            return JsonResponse(response_data)

    return JsonResponse({})
