from django import forms

class AddPageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=140)    
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":1, "cols":1}),label='Body')
    
   