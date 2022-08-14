from django import forms
from django.contrib.auth.models import User

from someapp.models import Message

class MessageForm(forms.Form):
    # from_user = forms.CharField(max_length=20)
    # to_user= forms.CharField(max_length=20)
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
        print('save ----req user',self.request.user)
        print('cleaned data',self.cleaned_data)
        print('cleaned data',self.data)
        print('from_user',self.from_user)
        print('to_user',self.to_user)
        #insecure design
        message = Message.objects.create(
            from_user=self.from_user,
            to_user=self.to_user,
            content=self.cleaned_data['content']
        )

        #a more secure design
        # message = Message.objects.create(
        #     from_user=self.request.user,
        #     to_user=self.cleaned_data['to_user'],
        #     content=self.cleaned_data['content']
        # )