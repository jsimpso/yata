from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from . import forms, models


@require_http_methods(["GET"])
def index(request):

    form = forms.CreateTodoForm()
    todos = models.TodoItem.objects.all()
    context = {"todo_items": todos, "form": form}
    return render(request, "todos/index.html", context)


@require_http_methods(["POST"])
def action_add_new_todo(request):
    form = forms.CreateTodoForm(request.POST)
    instance = form.save()
    return render(
        request,
        "todos/action_add_new_todo.html",
        {"item": instance},
    )


@require_http_methods(["PUT"])
def action_toggle_todo(request, item_id):
    item = models.TodoItem.objects.get(id=item_id)
    item.completed = not item.completed
    item.save()
    classes = ["font-semibold", "text-gray-900"]
    if item.completed:
        # response = f"<s>{item.title}</s>"
        classes.append("line-through")

    # else:
    #     response = item.title

    html_response = f"""
    <label id="checkbox-label-{item.id}"
           for="checkbox"
           class="{' '.join(classes)}">{item.title}</label>"""
    return HttpResponse(html_response)
