import ast
import io
from django.contrib.auth.models import AnonymousUser

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import FileResponse
from django_tex.core import *
from django_tex.response import PDFResponse
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import *
from .forms import CreateTaskForm, CreateExamForm, UpdateTaskForm, CreateTaskForm, UpdateTasksTextForm
from taggit.models import Tag

# Create your views here.


def task_overview(request):
    return render(request, "exam_organization/task_overview.html", {})


def index_view(request):
    return render(request, 'exam_organization/index.html')


def task_overview_view(request):
    form = FilterTasksForm()
    tasks = Task.objects.all()
    common_tags = Task.tags.most_common()[:6]

    if request.method == 'POST':

        form = FilterTasksForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']

            keywords = keywords.split(' ')
            tasks = Task.objects.none()

            for begriff in keywords:

                tasks |= Task.objects.filter(
                    Q(headline__contains=begriff)
                    | Q(description__contains=begriff)
                    | Q(tags__name__contains=begriff)
                ).distinct()

    context = {
        'form': form,
        'tasks': tasks,
        'common_tags': common_tags,
    }

    return render(request, 'exam_organization/task_overview.html', context)


@login_required
def own_task_overview_view(request):

    form = FilterTasksForm()
    tasks = Task.objects.filter(created_by=request.user)

    if request.method == 'POST':
        form = FilterTasksForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']

            keywords = keywords.split(' ')
            tasks_filter = Task.objects.none()

            for begriff in keywords:

                tasks_filter |= tasks.filter(
                    Q(headline__contains=begriff)
                    | Q(description__contains=begriff)
                    | Q(tags__name__contains=begriff)
                ).distinct()
            tasks = tasks_filter

    context = {
        'form': form,
        'tasks': tasks,
    }

    return render(request, 'exam_organization/own_task_overview.html', context)


def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    context = {
        'task': task
    }
    return render(request, 'exam_organization/task_detail.html', context)


def tagged_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    tasks = Task.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'tasks': tasks
    }
    return render(request, 'exam_organization/task_overview.html', context)


@login_required
def task_create_view(request):
    form = CreateTaskForm(request.user)
    if request.method == 'POST':
        form = CreateTaskForm(request.user, request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():

            task = form.save()
            if len(images) > 0:
                for file in images:
                    with open(os.path.join(settings.BASE_DIR, 'media', 'latex', str(form.instance.id) + "_" + file.name), 'wb+') as a:
                        a.write(file.read())

            return redirect(reverse('exam_organization:task_update', kwargs={'pk': form.instance.id}))

    context = {
        'form': form,
    }

    return render(request, 'exam_organization/task_create.html', context)


@login_required
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = UpdateTaskForm(request.user, instance=task)

    if request.method == 'POST':
        form = UpdateTaskForm(request.user, request.POST, instance=task)
        images = request.FILES.getlist('images')
        if form.is_valid():
            if len(images) > 0:
                for file in images:
                    with open(os.path.join(settings.BASE_DIR, 'media', 'latex', str(task.id) + "_" + file.name), 'wb+') as a:
                        a.write(file.read())
            form.save()
        context = {
            'form': UpdateTaskForm(request.user, instance=task),
            'task': task
        }

        return render(request, 'exam_organization/task_update.html', context)

    context = {
        'form': form,
        'task': task
    }
    return render(request, 'exam_organization/task_update.html', context)


@login_required
def task_delete_view(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect(reverse_lazy('exam_organization:task_overview'))
    return render(request, 'exam_organization/task_delete_confirm.html')


def create_pdf_preview(request, pk):
    template_name = 'latex/preview.tex'
    task = get_object_or_404(Task, id=pk)
    context = {
        'task_text': task.task_text,
        'latex_dir': os.path.join(settings.BASE_DIR, 'exam_organization', 'templates', 'latex')
    }
    try:
        file = open(os.path.join(settings.MEDIA_ROOT,
                    'pdf', str(task.id) + '.pdf'), 'rb')
        return FileResponse(file, as_attachment=False, filename=pk+".pdf")
    except:
        pdf = compile_template_to_pdf(template_name, context)
        print(template_name)
        with open(os.path.join(settings.MEDIA_ROOT,
                               'pdf', str(task.id) + '.pdf'), 'wb+') as file:
            file.write(pdf)

        buffer = io.BytesIO(pdf)

        return FileResponse(buffer, as_attachment=False, filename=f'{pk}.pdf')


def prepare_create_exam(request):
    if request.user.is_authenticated:
        try:
            sig = request.user.first_name[0] + ". " + request.user.last_name
        except:
            sig = ""
    else:
        sig = ""
    form = CreateExamForm(
        initial={'gruss': 'Viel Erfolg!', 'signatur': sig})
    context = {
        'form': form,
        'tasks_ids': request.GET.getlist('aid')
    }

    if request.method == 'POST':
        form = CreateExamForm(request.POST)

        if '' in dict(request.POST)['tasks_reihenfolge']:
            messages.add_message(request, messages.WARNING, 'Bitte die Reihenfolge einstellen.')
            context['alert'] = ('Bitte die Reihenfolge einstellen.', 'warning')
            return render(request, 'exam_organization/prepare_create_exam.html', context)
        if form.is_valid():

            request.session['tasks_reihenfolge'] = dict(
                request.POST)['tasks_reihenfolge']
            request.session['datum'] = dict(request.POST)['datum'][0]
            request.session['klasse'] = dict(request.POST)['klasse'][0]
            request.session['bezeichnung'] = dict(
                request.POST)['bezeichnung'][0]
            request.session['newpage_after'] = newpage_after = [
                key.split('_')[-1] for key in dict(request.POST).keys() if 'newpage_after_' in key]
            request.session['gruss'] = dict(request.POST)['gruss'][0]
            request.session['signatur'] = dict(request.POST)['signatur'][0]
            return redirect(reverse('exam_organization:prepare_create_exam_tasks'))

    return render(request, 'exam_organization/prepare_create_exam.html', context)


def prepare_create_exam_tasks(request):

    forms = []
    for id in request.session['tasks_reihenfolge']:
        task = get_object_or_404(Task, id=id)
        forms.append(UpdateTasksTextForm(instance=task))
    context = {'forms': forms}
    if request.method == 'POST':
        request.session['headlines'] = dict(request.POST)['headline']
        request.session['task_texte'] = dict(request.POST)['task_text']

        return create_exam(request)

    return render(request, 'exam_organization/prepare_create_exam_tasks.html', context)


def create_exam(request):
    template_name = 'latex/exam.tex'

    if request.method == "POST":

        post_dict = dict(request.POST)
        del post_dict['csrfmiddlewaretoken']

        tasks_ids = request.session['tasks_reihenfolge']

        newpage_after = [
            key.split('_')[-1] for key in post_dict.keys() if 'newpage_after_' in key]

        tasks = Task.objects.none()
        for task_id in tasks_ids:
            tasks |= Task.objects.filter(pk=task_id)

        inputs = ''
        total_BE = 0
        counter = 0
        for id in tasks_ids:
            counter += 1
            task = Task.objects.get(id=id)
            if not',' in task.total_BE:
                points = list(task.total_BE)
            else:
                points = ast.literal_eval(task.total_BE)
            text = request.session['task_texte'][counter-1]
            headline = request.session['headlines'][counter-1]
            inputs += '\\begin{aufgabe}[ ('
            for total_BE in points:
                total_BE += int(total_BE)
                inputs += str(total_BE) + " BE + "
            inputs = inputs[:-3]
            inputs += ")]\n"
            inputs += "\\textbf{" + headline + "}\n\n"
            inputs += text + '\n \\end{aufgabe}'
            if str(counter) in newpage_after:
                inputs += "\\nextpage\\newpage"

        context = {
            'latex_dir': os.path.join(settings.BASE_DIR, 'exam_organization', 'templates', 'latex'),
            'loesung': '0',
            'bezeichnung': request.session['bezeichnung'],
            'klasse': request.session['klasse'],
            'datum': request.session['datum'],
            'inputs': inputs,
            'gesamt_BE': str(total_BE),
            'gruss': request.session['gruss'],
            'signatur': request.session['signatur']}
        pdf = compile_template_to_pdf(template_name, context)

        return PDFResponse(pdf, filename="sa.pdf")
