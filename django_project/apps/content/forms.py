from django import forms
from .models import Publication, Comment, Rating

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'category', 'content', 'is_exclusive', 'is_breaking']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть заголовок'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_exclusive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_breaking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Заголовок новини',
            'content': 'Текст новини',
            'is_exclusive': 'Це Premium контент?',
            'is_breaking': 'Це термінова новина?',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишіть ваш коментар тут...'
            }),
        }
        labels = {
            'text': ''
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.Select(choices=[
                (5, '⭐⭐⭐⭐⭐ (5/5)'),
                (4, '⭐⭐⭐⭐ (4/5)'),
                (3, '⭐⭐⭐ (3/5)'),
                (2, '⭐⭐ (2/5)'),
                (1, '⭐ (1/5)'),
            ], attrs={'class': 'form-select'}),
        }
        labels = {
            'value': 'Ваша оцінка'
        }