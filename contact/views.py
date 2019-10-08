from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage

from .forms import ContactForm


def contact_us(request):

    # email address receiving contact form submissions:
    recipient = ['myemailadress@gmail.com']

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']

            message = EmailMessage(subject=f"New message from {sender_name} ({sender_email})",
                                   body=form.cleaned_data['message'], to=recipient)

            message.send()

            if form.cleaned_data['cc_myself']:

                cc_msg = EmailMessage(subject=f"Thank you for your message, {sender_name}.",
                                      body=f"We will get back to you shortly. "
                                      f"A copy of your message can be found below.\n\n"
                                      f"{form.cleaned_data['message']}", to=[sender_email])
                cc_msg.send()

            return HttpResponseRedirect('/')
            # TODO: create 'thanks for contacting us' page

    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
