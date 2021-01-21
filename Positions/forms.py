from attr.filters import exclude
from django import forms
from .models import Groups, Xyz, Positions, Levels, Persons, Change_types, Objects, Сhange_qality


class GroupsModelForm(forms.ModelForm):
    class Meta:
        model = Groups
        exclude=["id"]

class XyzModelForm(forms.ModelForm):
    class Meta:
        model = Xyz
        exclude=["id"]

class PositionsModelForm(forms.ModelForm):
    class Meta:
        model = Positions
        exclude=["id"]

class LevelsModelForm(forms.ModelForm):
    class Meta:
        model = Levels
        exclude=["id"]

class PersonsModelForm(forms.ModelForm):
    class Meta:
        model = Persons
        exclude=["id"]

class Change_typesModelForm(forms.ModelForm):
    class Meta:
        model = Change_types
        exclude=["id"]

class ObjectsModelForm(forms.ModelForm):
    class Meta:
        model = Objects
        exclude=["id"]

class Сhange_qalityModelForm(forms.ModelForm):
    class Meta:
        model = Сhange_qality
        exclude=["id"]