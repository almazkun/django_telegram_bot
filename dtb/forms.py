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
    )
    auth_token = forms.CharField(
        label="Auth Token",
        widget=forms.TextInput(
            attrs={"placeholder": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
        ),
    )

    class Meta:
        model = Bot
        fields = ("name", "auth_token")

    def save(self, commit=True):
        try:
            bot = BotCreate(
                domain=self.domain,
                bot_name=self.cleaned_data["name"],
                bot_token=self.cleaned_data["auth_token"],
                user=self.user,
            ).perform()
        except Exception as e:
            Bot.objects.filter(
                created_by=self.user, auth_token=self.cleaned_data["auth_token"]
            ).delete()
            self.add_error(None, e)
            raise e
        return bot
