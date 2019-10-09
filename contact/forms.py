from django import forms
import requests
from . import utilities


class ContactForm(forms.Form):

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ContactForm, self).__init__(*args, **kwargs)

    def verify_recaptcha(self):
        """
        makes API call to verify a user's google captcha response
        """
        # user response token provided by reCAPTCHA client-side integration:
        captcha_response = self.request.POST["g-recaptcha-response"]

        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            'secret': utilities.get_recaptcha_key(),
            'response': captcha_response,
            'remoteip': utilities.get_client_ip(self.request)
        }

        verify_rs = requests.get(url, params=params, verify=True)

        verify_rs = verify_rs.json()

        status = verify_rs.get("success", False)

        if not status:

            raise forms.ValidationError('Captcha Validation Failed.', code='invalid')



