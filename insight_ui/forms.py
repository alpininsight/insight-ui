from django import forms


class ChatForm(forms.Form):
    """A very simple chat form with only a message."""

    msg = forms.CharField()
