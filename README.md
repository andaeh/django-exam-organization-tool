# Django Exam Organization Tool

A tool to organize exam tasks seperately and join them into an exam.

## Language

The default language is german. You have to change several entries in different files.

## Requirements

This app uses Django as well as several django-modules, listed in requirements.txt. To install all required modules use `pip install -r requirements.txt`.

Also you need to have LaTeX installed on your system, e. g. [TeXLive](https://www.tug.org/texlive/).

## Change LaTeX-Output

To change LaTeX output edit "exam.tex" in "exam_organization/templates/latex". There you'll also find several configuration files. Feel free to use your own preamble.

