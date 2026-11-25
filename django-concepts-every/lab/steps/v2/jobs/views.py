from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Job, Task


def open_tasks(request):
    tasks = Task.objects.filter(done=False).order_by("job__address", "room")
    return render(request, "jobs/open.html", {"tasks": tasks})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.job = job
        task.save()
        return redirect(f"/jobs/{job.pk}/")
    return render(request, "jobs/job.html", {"job": job, "form": form})


@login_required
def my_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user, done=False)
    return render(request, "jobs/mine.html", {"tasks": tasks})
