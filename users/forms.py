from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from users.models import User


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'text-align: center;'


class LoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None

    def clean_phone(self):
        cleaned_data = self.cleaned_data.get('phone')
        if cleaned_data:
            for sign in list(cleaned_data):
                if sign.isalpha():
                    raise ValidationError('Номер телефона не должен содержать буквы!')

            return cleaned_data.strip()