from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from core.models import (
    User,

)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "name",
            "password",
            "mobile",
            "is_active",
            "is_admin",

        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "name",
            "password",
            "mobile",
            "is_active",
            "is_admin",

        ]


class UserAdmin(BaseUserAdmin):
    """Define the admin page for users."""

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ["id"]
    list_display = [
        "id",
        "email",
        "name",
        "mobile",
        "is_active",
        "is_admin",
    ]
    fieldsets = (
        (_("Securets"), {"fields": ("mobile", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "email",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",

                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    list_filter = (
        "id",
        "email",
        "name",
        "mobile",
        "is_active",
        "is_admin",
    )
    search_fields = ("id", "email", "name", "mobile", "is_active", "is_admin")
    add_fieldsets = (
        (
            _("User Details"),
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "mobile",
                    "is_active",
                    "is_admin",

                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)

