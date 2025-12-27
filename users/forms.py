from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User, UserProfile
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].help_text = None
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email'] 
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_image']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.HiddenInput(), required=False)
    username_or_email = forms.CharField(
        label="Email or Username", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Registered Email or Username'}),
        max_length=254
    )
    def clean(self):
        cleaned_data = super().clean()
        query = cleaned_data.get('username_or_email')
        if query:
            User = get_user_model()
            users = list(User.objects.filter(email__iexact=query))
            if not users:
                users = list(User.objects.filter(username__iexact=query))
            if users:
                cleaned_data['email'] = users[0].email
            else:
                cleaned_data['email'] = "noreply@example.com"
        return cleaned_data
class AdminEmailForm(forms.Form):
    subject = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%;'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows': 10, 'style': 'width: 100%;'}),
        required=True
    )
