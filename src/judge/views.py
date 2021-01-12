from django.conf import settings
from django.shortcuts import render, Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView
from datetime import datetime as dt
from difflib import ndiff
from .forms import LanguageForm, SubmitSolutionForm
from .memory_test import display_top
from .models import Task
from .service import get_all_available_tasks, get_task_by_number, submit_solution
# from .models import Text, CodeFile
 
 
import os
import subprocess
import functools
import time
import tracemalloc
import logging
 

logger = logging.getLogger(__name__)


def api_show_language_dropdown(request):
    if request.method == 'GET':
        language_form = LanguageForm()
    return render(request, 'judge/language.html', {'form': language_form})


class TaskDetailView(DetailView):
    model = Task
    slug_field = 'number'
    template = 'judge/task_detail.html'
    queryset = get_all_available_tasks()

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return get_task_by_number(slug)
        except:
            raise Http404(_('Task not found'))


def api_submit_solution(request, slug):
    if request.method == 'POST':
        form = SubmitSolutionForm(request.POST)
        if form.is_valid():
            submit_solution(
                task_number=request.POST.get('task_number'),
                programming_language=request.POST.get('programming_language'),
                source_code=request.POST.get('source_code')
            )
    else:
        form = SubmitSolutionForm()
    return render(request, 'judge/submit_solution.html', {'form': form, 'task_number': slug})


# class TextCreate(CreateView):
 
 
#     model = Text
#     form_class = TextForm
#     template_name = 'judge/create.html'
 
#     def form_valid(self, form):
#         text = form.save(commit=False)
#         if not os.path.exists(settings.MEDIA_ROOT): 
#             os.makedirs(settings.MEDIA_ROOT)
 
 
#         # code for c++ 
#         with open(f'{os.path.join(settings.MEDIA_ROOT, "main.cpp")}', 'w', encoding='utf-8') as file:
#             print(text.text, file=file, end='')
 
 
#         try:
#             cfile = os.path.join(settings.MEDIA_ROOT, 'main.cpp')
#             ofile = os.path.join(settings.MEDIA_ROOT, 'main')
#             efile = os.path.join(settings.MEDIA_ROOT, 'main.exe')
#             command_string = 'g++ ' + cfile + ' -o ' + ofile
#             compile_result = subprocess.check_output(command_string,stderr=subprocess.STDOUT,shell=True)
#             if compile_result != "": #compile successfull
#                 command_string = f"{ofile} < {ofile}Input.txt > {ofile}Output.txt"
#                 # with open('output.txt', 'w', encoding='utf-8') as file:
#                 #     print(command_string, file=file)
 
 
#         #code for python
#         # with open(f'{settings.MEDIA_ROOT}\\main.py', 'w', encoding='utf-8') as file:
#         #     print(text.text, file=file, end='')
 
#         # try:
#         #     python_file = os.path.join(settings.MEDIA_ROOT, 'main.py')
#         #     command_string = f'python { python_file } < {python_file[:-3]}Input.txt > {python_file[:-3]}Output.txt'
#         #     with open('output.txt', 'w', encoding='utf-8') as file:
#         #         print (f"{command_string}", file=file)
 
#             # check results
#             # compile_result = subprocess.check_output(command_string,stderr=subprocess.STDOUT,shell=True)
            
#             start_time = time.time()
#             tracemalloc.start()
#             compile_result = os.system(f'cmd /c "{command_string}"')
#             start_time = time.time() - start_time
#             snapshot = tracemalloc.take_snapshot()
 
#             with open(f'{ofile}Output.txt', 'r') as file1, open(f'{ofile}Check.txt', 'r') as file2:
#             # with open(f'{python_file[:-3]}Output.txt', 'r') as file1, open(f'{python_file[:-3]}Check.txt', 'r') as file2:
#                 file_1 = file1.readlines()
#                 file_1 = [line.rstrip() for line in file_1]
#                 file_2 = file2.readlines()
#                 file_2 = [line.rstrip() for line in file_2]
#             with open('output.txt', 'w', encoding='utf-8') as file:
#                 # print(''.join(ndiff(file_1, file_2)), file=file)
#                 if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,file_1,file_2), True):
#                     print (f"Списки одинаковые\n{start_time}", file=file)
#                 else:
#                     print (f"Списки не одинаковые", file=file)
#             display_top(snapshot)
#         except:
#             pass
#         return super().form_valid(form)
 
 
# # class FileExecute(CreateView):
# #     model = CodeFile
# #     form_class = CodeFileForm
# #     template_name = 'loader/create.html'
 
# #     def form_valid(self, form):
# #         if not os.path.exists(settings.MEDIA_ROOT): 
# #             os.makedirs(settings.MEDIA_ROOT)
# #          try:
# #             cfile = os.path.join(settings.MEDIA_ROOT, 'main.cpp')
# #             ofile = os.path.join(settings.MEDIA_ROOT, 'main')
# #             efile = os.path.join(settings.MEDIA_ROOT, 'main.exe')
# #             command_string = 'g++ ' + cfile + ' -o ' + ofile
# #             compile_result = subprocess.check_output(command_string,stderr=subprocess.STDOUT,shell=True)
# #             if compile_result != "": #compile successfull
# #                 command_string = ofile
# #                 compile_result = subprocess.check_output(command_string,stderr=subprocess.STDOUT,shell=True)
# #         except:
# #             pass