import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from dtb.models import Bot, Predictor
from dtb.usecases import bot_create, chat_gpt_create

logger = logging.getLogger(__name__)


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
    auth_token = forms.CharField(
        label="Auth Token",
        widget=forms.TextInput(
            attrs={"placeholder": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"}
        ),
        required=True,
        help_text="You can get it from <a href='https://t.me/BotFather'>@BotFather</a>",
    )

    class Meta:
        model = Bot
        fields = ("auth_token",)

    def clean_auth_token(self):
        auth_token = self.cleaned_data["auth_token"]
        try:
            self.bot_created = bot_create.BotCreate(auth_token)
            self.bot_created._get_me()
        except Exception as e:
            logger.exception(e)
            raise forms.ValidationError("Invalid auth token.")
        return auth_token

    def save(self, commit=True):
        try:
            self.bot_created.perform(
                user=self.user,
                domain=self.domain,
            )
        except Exception as e:
            logger.exception(e)
            raise forms.ValidationError("Something went wrong.")


class PredictorCreateForm(BootstrapFormMixin, forms.ModelForm):
    api_key = forms.CharField(
        label="OpenAI API Key",
        widget=forms.TextInput(
            attrs={
                "placeholder": "sk-proj-111111111111111111111111111111111111111111111111"
            }
        ),
        required=True,
        help_text="You can get it from <a href='https://platform.openai.com/api-keys'>OpenAI</a>",
    )

    class Meta:
        model = Predictor
        fields = ("api_key",)

    def __init__(self, *args, bot, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    def save(self, commit=True):
        predictor = super().save(commit=False)
        predictor.bot = self.bot
        predictor.context = chat_gpt_create.generate_initial_prompt()
        if commit:
            predictor.save()
        return predictor


class PredictorUpdateForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["api_key"] = self.get_api_key_field()

    context = forms.CharField(
        label="System Prompt",
        widget=forms.Textarea(
            attrs={"placeholder": "Once upon a time, there was a chatbot..."}
        ),
        required=False,
        help_text="The prompt that will be used to generate responses.",
    )

    class Meta:
        model = Predictor
        fields = ("api_key", "context")

    def get_api_key_field(self):
        return forms.CharField(
            label="OpenAI API Key",
            widget=forms.PasswordInput(
                attrs={
                    "placeholder": "sk-proj-111111111111111111111111111111111111111111111111"
                }
            ),
            required=False,
            help_text="You can get it from <a href='https://platform.openai.com/api-keys'>OpenAI</a>",
        )
