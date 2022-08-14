from django import forms
from django.contrib.auth.models import User

from someapp.models import Message

class MessageForm(forms.Form):
    
    content = forms.CharField(widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        request=kwargs.pop('request')
        self.request=request
        initial= kwargs.pop('initial')
        self.from_id=initial['from_user']
        self.to_user_id=initial['to_user']
        super(MessageForm, self).__init__(*args, **kwargs)
        from_user = User.objects.get(id=self.from_id)
        to_user=User.objects.get(id=self.to_user_id)
        self.from_user=from_user
        self.to_user=to_user

    def save(self):
        #insecure design. Sender can be manipulated by changing the address bar
        message = Message.objects.create(
            from_user=self.from_user,
            to_user=self.to_user,
            content=self.cleaned_data['content']
        )

        #a more secure design. The sender can't be atleast that easily manipulated
        # message = Message.objects.create(
        #     from_user=self.request.user,
        #     to_user=self.to_user,
        #     content=self.cleaned_data['content']
        # )