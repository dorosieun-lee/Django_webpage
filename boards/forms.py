from django import forms
from .models import Board, Comment

class BoardForm(forms.ModelForm):
    title = forms.CharField(
        label='제목 ',
        widget=forms.TextInput(
            attrs={
                'placeholder':'제목을 입력하세요.'
            }
        )
    )
    content = forms.CharField(
        label='내용 ',
        widget=forms.Textarea(
            attrs={
                'placeholder':'내용을 입력하세요.'
            }
        )
    )
    class Meta:
        model = Board
        fields = ('title', 'content', )

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='댓글 ',
        widget=forms.TextInput(
            attrs={
                'placeholder':'내용을 입력하세요.'
            }
        )
    )
    class Meta:
        model = Comment
        fields = ('content', )