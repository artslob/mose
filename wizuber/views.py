from django.shortcuts import render, get_object_or_404

from wizuber.models import Wizard


def index(request):
    return render(request, 'wizuber/index.html')


def wizards(request):
    all_wizards = Wizard.objects.all()
    return render(request, 'wizuber/wizards.html', dict(wizards=all_wizards))


def wizard_detail(request, wizard_id):
    return render(request, 'wizuber/wizard_detail.html', dict(question=get_object_or_404(Wizard, pk=wizard_id)))
