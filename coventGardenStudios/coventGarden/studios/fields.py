from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import CustomPasswordValidator

"""
Arguments
"""
# Lengths
LENGTH_NAME = 150       # Name field maximum length is 150 (See django.contrib.auth)
LENGTH_PASSWORD = 255   # Password maximum length value is 4096
LENGTH_EMAIL = 320      # Email maximum length value
LENGTH_PHONE = 10       # Phone number default length value
LENGTH_URL = 200        # URL default length value
LENGTH_TEXT = 5000

# Labels
LABEL_USERNAME = "Nom d'utilisateur"
LABEL_FIRST_NAME = "Prénom"
LABEL_LAST_NAME = "Nom"
LABEL_GROUP_NAME = "Nom de groupe"
LABEL_EMAIL = "Adresse e-mail"
LABEL_PHONE = "Numéro de téléphone"
LABEL_PASSWORD = "Mot de passe"
LABEL_PASSWORD_CURRENT = "Mot de passe actuel"
LABEL_PASSWORD_CONFIRM = "Confirmer le mot de passe"



"""
Forms
"""
# Widgets
WIDGET_TEXT = forms.TextInput(attrs={'class': 'form-control'})
WIDGET_EMAIL = forms.EmailInput(attrs={'class': 'form-control'})
WIDGET_PASSWORD = forms.PasswordInput(attrs={'class': 'form-control'})

# Forms
FORM_USERNAME = forms.CharField(max_length=LENGTH_NAME, label=LABEL_USERNAME, widget=WIDGET_TEXT)
FORM_EMAIL = forms.EmailField(max_length=LENGTH_EMAIL, label=LABEL_EMAIL, widget=WIDGET_EMAIL)
FORM_PASSWORD = forms.CharField(max_length=LENGTH_PASSWORD, label=LABEL_PASSWORD, widget=WIDGET_PASSWORD)
FORM_PASSWORD_NEW = forms.CharField(max_length=LENGTH_PASSWORD, label=LABEL_PASSWORD, widget=WIDGET_PASSWORD, validators=CustomPasswordValidator)
FORM_PASSWORD_CONFIRM = forms.CharField(max_length=LENGTH_PASSWORD, label=LABEL_PASSWORD_CONFIRM, widget=WIDGET_PASSWORD)



"""
Models
"""
# Error messages
UNIQUE_USERNAME = {"unique": "Ce nom d'utilisateur est déjà utilisé"}
UNIQUE_EMAIL = {"unique": "Cette adresse email est déjà utilisée."}

# CustomUser
MODEL_USERNAME = models.CharField(max_length=LENGTH_NAME, verbose_name=LABEL_USERNAME, unique=True, error_messages=UNIQUE_USERNAME)
MODEL_EMAIL = models.EmailField(max_length=LENGTH_EMAIL, verbose_name=LABEL_EMAIL, unique=True, error_messages=UNIQUE_EMAIL)
MODEL_LAST_NAME = models.CharField(max_length=LENGTH_NAME, verbose_name=LABEL_FIRST_NAME)
MODEL_FIRST_NAME = models.CharField(max_length=LENGTH_NAME, verbose_name=LABEL_LAST_NAME)
MODEL_PHONE = models.CharField(max_length=LENGTH_PHONE, verbose_name=LABEL_PHONE)
MODEL_PASSWORD = models.CharField(max_length=LENGTH_PASSWORD, verbose_name=LABEL_PASSWORD, validators=CustomPasswordValidator)
MODEL_PASSWORD_CONFIRM = models.CharField(max_length=LENGTH_PASSWORD, verbose_name=LABEL_PASSWORD_CONFIRM, blank=True, null=True)

# CustomGroup
MODEL_GROUP_NAME = models.CharField(max_length=LENGTH_NAME, verbose_name="Nom de groupe", blank=True)
MODEL_GROUP_EMAIL = models.EmailField(max_length=LENGTH_EMAIL, verbose_name="E-mail", blank=True)
MODEL_GROUP_PHONE = models.CharField(max_length=LENGTH_PHONE, verbose_name="Numéro de téléphone", blank=True)
MODEL_MEMBERS = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)], verbose_name="Nombre de membres", default=1, blank=True)
MODEL_GENRE = models.CharField(max_length=LENGTH_NAME, verbose_name="Style musicale", blank=True)
MODEL_FACEBOOK = models.URLField(max_length=LENGTH_URL, blank=True)
MODEL_INSTAGRAM = models.URLField(max_length=LENGTH_URL, blank=True)
MODEL_BIOGRAPHY = models.TextField(max_length=LENGTH_TEXT, verbose_name="Biographie", blank=True)
MODEL_TECHNICAL_SHEET = models.FileField(upload_to='media/public', verbose_name="Fiche technique", blank=True, null=True)
MODEL_LOGO = models.FileField(upload_to='media/public', verbose_name="Logo", blank=True, null=True)
MODEL_VALIDATED = models.BooleanField(default=False, verbose_name="Vérifié", blank=True)
