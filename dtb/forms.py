from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from dtb.models import Bot
from dtb.usecases.bot_create import BotCreate


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control form-control-sm"
            if field.help_text:
                field.help_text = (
                    f'<small class="form-text text-muted">{field.help_text}</small>'
                )


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2")


class BotCreateForm(BootstrapFormMixin, forms.ModelForm):
    name = forms.CharField(
        label="Bot Name",
        widget=forms.TextInput(attrs={"placeholder": "My Bot"}),
        required=True,
        help_text="This name will be displayed in the list of your bots",
    )
    auth_token = forms.CharField(
        label="Auth Token",
        widget=forms.TextInput(
            attrs={"placeholder": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
        ),
        required=True,
        help_text="You can get it from <a href='https://t.me/BotFather'>BotFather</a>",
    )

    class Meta:
        model = Bot
        fields = ("name", "auth_token")

    def clean_auth_token(self):
        try:
            auth_token = self.cleaned_data["auth_token"]
            self.bot_create = BotCreate(auth_token)
            self.bot_create.validate().result()
        except Exception:
            raise forms.ValidationError("Invalid auth token")
        return auth_token

    def save(self, commit=True):
        try:
            return self.bot_create.perform(
                name=self.cleaned_data["name"],
                auth_token=self.cleaned_data["auth_token"],
                user=self.user,
                domain=self.domain,
            )
        except Exception:
            Bot.objects.filter(
                created_by=self.user, auth_token=self.cleaned_data["auth_token"]
            ).delete()
            raise forms.ValidationError("Something went wrong, please try again later")
