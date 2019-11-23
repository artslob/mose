from django.forms import ModelForm

from wizuber.models import CandleArtifact


class CandleArtifactForm(ModelForm):
    class Meta:
        model = CandleArtifact
        exclude = ['wish']
