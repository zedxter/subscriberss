from django import forms

class SubscribeForm(forms.Form):
    email = forms.EmailField()
    feed_link = forms.URLField(verify_exists=True)
