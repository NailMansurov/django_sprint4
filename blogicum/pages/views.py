from django.shortcuts import render
from django.views.generic import TemplateView
from http import HTTPStatus


class AboutPage(TemplateView):
    """Статичная страница. О проекте Блогикум."""

    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """Статичная страница. Правила проекта Блогикум."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=HTTPStatus.NOT_FOUND)


def server_error(request):
    return render(request, 'pages/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=HTTPStatus.FORBIDDEN)
