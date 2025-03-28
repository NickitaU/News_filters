from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from news.models import Author


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        # Добавляем пользователя в группу
        authors_group.user_set.add(user)

        # Создаем запись в таблице Author
        Author.objects.get_or_create(user=user)

    return redirect('/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
