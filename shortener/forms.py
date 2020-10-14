  
from django import forms
from .validators import validate_url
from .models import Message




class SubmitUrlForm(forms.Form):
    url = forms.CharField(
            label='', 
            validators=[validate_url],
            widget = forms.TextInput(
                    attrs ={
                        "placeholder": "Enter the link here",
                        "class": "form-control"
                        }
                )
            )

    def clean_url(self):
        url = self.cleaned_data['url']
        if "http" in url:
            return url
        return "http://" + url


class MessageForm(forms.ModelForm):
    math1=forms.IntegerField(widget=forms.HiddenInput())
    math=forms.IntegerField(label='' ,required=True)

    class Meta:
        model=Message
        fields=['username','email','content']
        labels = {
            "username": "Your name",
            'email':'Your email',
            'content':'Your message',
        }
    
    def clean_math(self):
        math1=self.cleaned_data['math']
        math=self.cleaned_data['math1']
        if math!=math1:
            raise forms.ValidationError('Your answer is incorrect!')
        return math

    def clean_content(self):
        con=self.cleaned_data['content']
        if len(con)<2:
            raise forms.ValidationError('Message is too short!')
        return con

class CounterForm(forms.Form):
     url = forms.CharField(
            label='', 
            validators=[validate_url],
            widget = forms.TextInput(
                    attrs ={
                        "placeholder": "Enter here your shortened URL",
                        "class": "form-control"
                        })
            )