from django import forms
from .models import TimeStamp, ForexEntry, BinaryEntry, Reason, Lesson


class ReasonForm(forms.Form):
    r_text = forms.CharField(label='Reasons', widget=forms.Textarea)
    r_image = forms.FileField(label='Reason Image')


class LessonForm(forms.Form):
    l_text = forms.CharField(label='Lessons', widget=forms.Textarea)
    l_image = forms.FileField(label='Lesson Image')


class StampForm(forms.ModelForm):
    option = forms.CharField(
        widget=forms.HiddenInput,
    )

    owner = forms.CharField(
        widget=forms.HiddenInput,
    )

    class Meta:
        model = TimeStamp
        fields = '__all__'


class ForexEntryForm(forms.ModelForm):
    SL = forms.FloatField(label='Stop Loss', required=True)
    TP = forms.FloatField(label='Take Profit', required=True)
    timeStart = forms.DateTimeField(label='Trade Start')
    timeEnded = forms.DateTimeField(label='Trade End')
    stamp = forms.UUIDField(
        widget=forms.HiddenInput,
    )

    class Meta:
        model = ForexEntry
        fields = '__all__'


class BinaryEntryForm(forms.ModelForm):
    stamp = forms.UUIDField(
        widget=forms.HiddenInput,
    )

    class Meta:
        model = BinaryEntry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pair'].widget.attrs.update(
            {
                'placeholder': 'Currency Traded'})
        self.fields['payout'].widget.attrs.update(
            {
                'placeholder': 'Payout Rate'})
