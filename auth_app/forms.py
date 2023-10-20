from django.contrib.auth.forms import UserCreationForm

from auth_app.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'surname', 'name', 'phone', 'password1', 'password2')
