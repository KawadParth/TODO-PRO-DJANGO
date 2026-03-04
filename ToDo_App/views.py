from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def task_list(request):
    if request.method == "POST":
        title = request.POST.get("task_name") # Matches the 'name' attribute in your HTML
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')

    # Fetch tasks
    upcoming_tasks = Task.objects.filter(is_completed=False)
    completed_tasks = Task.objects.filter(is_completed=True)
    
    # Calculate Progress Percentage
    total_count = Task.objects.count()
    completed_count = completed_tasks.count()
    
    # Avoid division by zero
    progress = 0
    if total_count > 0:
        progress = int((completed_count / total_count) * 100)

    context = {
        'upcoming_tasks': upcoming_tasks,
        'completed_tasks': completed_tasks,
        'progress': progress,
    }
    return render(request, 'todo/index.html', context)

def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('task_list')

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')