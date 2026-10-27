from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import TodoList, TodoItem


def index(request):
    todo_lists = TodoList.objects.all()
    return render(request, "todos/index.html", {"todo_lists": todo_lists})


def list_detail(request, list_id):
    todo_list = get_object_or_404(TodoList, pk=list_id)
    return render(request, "todos/list_detail.html", {"todo_list": todo_list})


@require_http_methods(["POST"])
def list_create(request):
    title = request.POST.get("title", "").strip()
    if title:
        todo_list = TodoList.objects.create(title=title)
        return redirect("list_detail", list_id=todo_list.id)
    return redirect("index")


@require_http_methods(["POST"])
def list_delete(request, list_id):
    todo_list = get_object_or_404(TodoList, pk=list_id)
    todo_list.delete()
    return redirect("index")


@require_http_methods(["POST"])
def item_create(request, list_id):
    todo_list = get_object_or_404(TodoList, pk=list_id)
    title = request.POST.get("title", "").strip()
    if title:
        TodoItem.objects.create(todo_list=todo_list, title=title)
    return redirect("list_detail", list_id=list_id)


@require_http_methods(["POST"])
def item_toggle(request, list_id, item_id):
    item = get_object_or_404(TodoItem, pk=item_id, todo_list_id=list_id)
    item.completed = not item.completed
    item.save()
    return redirect("list_detail", list_id=list_id)


@require_http_methods(["POST"])
def item_delete(request, list_id, item_id):
    item = get_object_or_404(TodoItem, pk=item_id, todo_list_id=list_id)
    item.delete()
    return redirect("list_detail", list_id=list_id)
