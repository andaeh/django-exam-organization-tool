import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelform_factory
from django.template.defaultfilters import slugify

from django_ace import AceWidget #https://github.com/django-ace/django-ace

from .models import *

# Custom login lorm
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-2',
        'placeholder': "Nutzer*innenname",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-2',
        'placeholder': "Passwort",
    }))

# Create form for tasks
class CreateTaskForm(forms.ModelForm):
    images = forms.CharField(
        required=False, 
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        help_text="Bitte alle Bilder hochladen, die in der Datei eingebunden werden.",
        label="Bilder"
        )
    
    class Meta:
        model = Task
        fields = ['headline', 'description', 'topic', 'total_BE', 'task_text', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
            'task_text': AceWidget( 
                mode='latex',
                theme='TextMate',
                wordwrap=True,
                width="100%",
                height="300px",
                minlines=None,
                maxlines=None,
                showprintmargin=False,
                showinvisibles=False,
                usesofttabs=True,
                tabsize=None,
                fontsize="18px",
                toolbar=False,
                readonly=False,
                showgutter=True,  # To hide/show line numbers
                behaviours=True,  # To disable auto-append of quote when quotes are entered
                )
        }
        help_texts = {
            'topic': 'STRG halten für die Auswahl mehrerer Bereiche'
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'


    def save(self, commit=True):
        instance = super(CreateTaskForm, self).save(commit=False)
        
        instance.created_by = self.user
        instance.edited_by = self.user
        
        number_tasks_with_headline = Task.objects.filter(headline__contains = instance.headline).count()
        print(number_tasks_with_headline)
        instance.slug = slugify(instance.headline + '_' + str(number_tasks_with_headline))
        print(instance.slug)

        instance.save()
        text = instance.task_text

        bracket_index = find_bracket_index_of_graphics(text)
        counter = 0
        for i in bracket_index:
            insert_start = i + 1 + counter * (len(str(instance.id)) + 1)
            insert_end = i + 1 + (counter + 1) * (len(str(instance.id)) + 1)
            if text[insert_start:insert_end] == str(instance.id) + "_":
                continue
            text = text[:insert_start] + str(instance.id) + "_" + text[insert_start:]
            counter += 1

        instance.task_text = text

        instance.save()
        self.save_m2m()
        
    
# Update form for tasks
class UpdateTaskForm(forms.ModelForm):
    images = forms.CharField(
        required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        help_text="Bitte alle Bilder hochladen, die in der Datei eingebunden werden.",
        label="Bilder"
    )
    
    class Meta:
        model = Task
        fields = ['headline', 'description', 'topic', 'total_BE', 'task_text', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
            'task_text': AceWidget( 
                mode='latex',
                theme='TextMate',
                wordwrap=True,
                width="100%",
                height="300px",
                minlines=None,
                maxlines=None,
                showprintmargin=False,
                showinvisibles=False,
                usesofttabs=True,
                tabsize=None,
                fontsize="18px",
                toolbar=False,
                readonly=False,
                showgutter=True,  # To hide/show line numbers
                behaviours=True,  # To disable auto-append of quote when quotes are entered
                )
        }
        help_texts = {
            'topic': 'STRG halten für die Auswahl mehrerer Bereiche'
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UpdateTaskForm, self).__init__(*args, **kwargs)
        
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        instance = super(UpdateTaskForm, self).save(commit=False)
        text = instance.task_text
        
        bracket_index = find_bracket_index_of_graphics(text)
        counter = 0
        for i in bracket_index:
            insert_start = i + 1 + counter * (len(str(instance.id)) + 1)
            insert_end = i + 1 + (counter + 1) * (len(str(instance.id)) + 1)
            if text[insert_start:insert_end] == str(instance.id) + "_":
                continue
            text = text[:insert_start] + str(instance.id) + "_" + text[insert_start:]
            counter += 1

        instance.task_text = text
        instance.edited_by = self.user
        number_of_tasks_with_headline = Task.objects.filter(headline = instance.headline).count()
        
        instance.slug = slugify(instance.headline + '_' + str(number_of_tasks_with_headline + 1))


        if commit:
            instance.save()

        self.save_m2m()


# Tasks keyword filter
# class FilterTasksForm(forms.Form):
#     keywords = forms.CharField(
#         label="Suchbegriffe",
#         required=False, 
#         widget=forms.TextInput(attrs={
#             'class': 'form-control'
#             }
#         ),
#     )

# Form for creating exams
class CreateExamForm(forms.Form):
    bezeichnung = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    klasse = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    datum = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control'
    }))
    gruss = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    signatur = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

# Update tasks before creation of exam
class UpdateTasksTextForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['headline', 'task_text']
                    
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'task_text': AceWidget( 
                mode='latex',
                theme='TextMate',
                wordwrap=True,
                width="100%",
                height="300px",
                minlines=None,
                maxlines=None,
                showprintmargin=False,
                showinvisibles=False,
                usesofttabs=True,
                tabsize=None,
                fontsize="18px",
                toolbar=False,
                readonly=False,
                showgutter=True,  # To hide/show line numbers
                behaviours=True,  # To disable auto-append of quote when quotes are entered
                )
        }
    

# function to find included graphics in LaTeX to add task-id to name
def find_bracket_index_of_graphics(text):
    graphics_startindex = [w.start() for w in re.finditer('\\\\includegraphics', text)]
    bracket_index = []
    for i in graphics_startindex:
        bracket_index.append(text.find("{", i))
    return bracket_index