from django import forms
from django.contrib.auth.models import User
from .models import ScheduledPost, SocialAccount
from .constants import PLATFORM_CHOICES, TIMEZONE_CHOICES
from django.utils import timezone


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords don't match!")
        
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters!")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ConnectAccountForm(forms.Form):
    platform = forms.ChoiceField(
        choices=PLATFORM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your account username'
        })
    )
    access_token = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Paste your API token or access token here'
        }),
        help_text="For demo: any text. For production: real OAuth token"
    )


class SchedulePostForm(forms.ModelForm):
    timezone = forms.ChoiceField(
        choices=TIMEZONE_CHOICES,
        initial='Asia/Kolkata',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = ScheduledPost
        fields = ['social_account', 'content', 'image', 'scheduled_at']
        widgets = {
            'social_account': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'What\'s on your mind? (max 280 chars)',
                'maxlength': '280'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'scheduled_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filter to only show connected accounts
            self.fields['social_account'].queryset = SocialAccount.objects.filter(
                user=user,
                is_connected=True
            )
    
    def clean(self):
        cleaned_data = super().clean()
        scheduled_at = cleaned_data.get('scheduled_at')
        content = cleaned_data.get('content')
        
        if not content or len(content.strip()) == 0:
            raise forms.ValidationError("Content cannot be empty!")
        
        if scheduled_at and scheduled_at <= timezone.now():
            raise forms.ValidationError("Scheduled time must be in the future!")
        
        return cleaned_data
