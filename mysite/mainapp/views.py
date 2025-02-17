from django.shortcuts import render

def index(request):
    return render(request, 'main_page/index.html')

def register(request):
    return render(request, 'main_page/register.html')

def find_friends(request):
    return render(request, 'main_page/find_friends.html')

def find_tutor_indiv(request):
    return render(request, 'main_page/find_tutor_indiv.html')

def find_tutor_group(request):
    return render(request, 'main_page/find_tutor_group.html')

def become_tutor(request):
    return render(request, 'main_page/become_tutor.html')
