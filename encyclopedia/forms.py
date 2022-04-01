from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 30, 'cols': 10}))
    editable = forms.BooleanField(widget = forms.HiddenInput(), required = False, initial=False)
