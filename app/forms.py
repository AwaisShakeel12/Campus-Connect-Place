from django import forms
from django.forms import ModelForm, CharField
from .models import ChatMessage, User

class ChatMessageForm(ModelForm):
    body= forms.CharField(widget=forms.Textarea(attrs={"class":"forms","rows":3,"placeholder":'type message'}))

    class Meta:
        model = ChatMessage
        fields = ['body',]

class AddFriendForm(forms.Form):
    friend_username = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a user")

    def clean_friend_username(self):
        friend = self.cleaned_data['friend_username']
        return friend
