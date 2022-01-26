from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .models import Question
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    latest_questions_list = Question.objects.order_by('question_text')[:5]

    context = {
        'latest_questions_list': latest_questions_list,
    }

    return render(request, 'questions/index.html', context)