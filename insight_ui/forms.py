from django import forms


class ChatForm(forms.Form):
    """A very simple chat form with only a message."""

    msg = forms.CharField()


class FormDemoForm(forms.Form):
    """Demo form for the form component demo."""

    title = forms.CharField(max_length=16)
    firstname = forms.CharField(max_length=32)
    lastname = forms.CharField(max_length=32)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.Textarea()
