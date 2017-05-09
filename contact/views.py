from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from .forms import ContactForm
from django.conf import settings


# Create your views here.

def contact_view(request):
    form = ContactForm(request.POST or None)

    if form.is_valid():
        send_mail("Contact from " + form.cleaned_data.get("email"), form.cleaned_data.get("message"),
                  settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
        return HttpResponseRedirect("/")

    context = {
        "form": form,
    }

    return render(request, "contact.html", context)
