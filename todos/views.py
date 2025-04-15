from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from . import forms


@require_http_methods(["GET"])
def index(request):

    form = forms.CreateTodoForm()
    context = {"form": form}
    return render(request, "todos/index.html", context)
