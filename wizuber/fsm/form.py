from django.forms import ModelForm

from wizuber.models import CandleArtifact, PentacleArtifact


class CandleArtifactForm(ModelForm):
    class Meta:
        model = CandleArtifact
        exclude = ['wish']


class PentacleArtifactForm(ModelForm):
    class Meta:
        model = PentacleArtifact
        exclude = ['wish']
