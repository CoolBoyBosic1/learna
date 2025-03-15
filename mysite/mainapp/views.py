from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import requests, json, csv, io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from django.db.models import Count
from .models import User, Subsubject, Subject
# APPS_SCRIPT_URL – це лінк на Apps Script
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbybx6jIcpQzdmGjfYvJcsxnj3pTNaBz2OpiILQgekBJAMYfTGbZLc-1FHe8XYn_u6shQw/exec"


def index(request):
    # Якщо натиснуто одну з кнопок (знайти друзів / репетитора тощо)
    if request.method == 'POST':
        user_choice = request.POST.get('choice')
        request.session['user_choice'] = user_choice
        if not request.user.is_authenticated:
            return redirect('register')
        else:
            return redirect('select_subject')

    # Читаємо CSV із Google-таблиці (матеріали)
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRi2gBCZN4CfzrQ7eH_rdCfSYY4LSHXR_cjddl3TNyh5YYH9WM-qjQw8qkck-eBLknGi4UvVR_EpVi4/pub?output=csv"
    resp = requests.get(csv_url)
    resp.encoding = 'utf-8'
    reader = csv.reader(io.StringIO(resp.text))
    headers = next(reader, None)  # пропускаємо заголовки
    materials = list(reader)

    return render(request, 'main_page/index.html', {
        'materials': materials
    })


def material_click(request, row_index):
    """
    Збільшує лічильник кліків (Apps Script) і редіректить на YouTube.
    """
    actual_row = row_index + 2
    data = {'rowIndex': actual_row}
    try:
        requests.post(APPS_SCRIPT_URL, data=data)
    except Exception as e:
        print("Помилка при оновленні лічильника:", e)

    # Знову читаємо CSV, щоб отримати посилання
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRi2gBCZN4CfzrQ7eH_rdCfSYY4LSHXR_cjddl3TNyh5YYH9WM-qjQw8qkck-eBLknGi4UvVR_EpVi4/pub?output=csv"
    resp = requests.get(csv_url)
    resp.encoding = 'utf-8'
    reader = csv.reader(io.StringIO(resp.text))
    headers = next(reader, None)
    materials = list(reader)

    try:
        youtube_link = materials[row_index][1]
    except IndexError:
        youtube_link = '/'
    return redirect(youtube_link)


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        city = request.POST.get('city')
        info = request.POST.get('info')
        role = request.POST.get('role', 'learner')

        if password1 != password2:
            messages.error(request, "Паролі не співпадають!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Користувач з таким email вже існує!")
            return redirect('register')

        if User.objects.filter(nickname=nickname).exists():
            messages.error(request, "Такий нікнейм вже існує!")
            return redirect('register')

        user = User.objects.create_user(
            email=email,
            nickname=nickname,
            password=password1,
            city=city,
            info=info,
            role=role
        )
        login(request, user)
        messages.success(request, "Ви успішно зареєструвалися!")

        user_choice = request.session.get('user_choice')
        if user_choice:
            return redirect('select_subject')
        else:
            return redirect('index')

    return render(request, 'main_page/register.html')


def select_subject(request):
    if not request.user.is_authenticated:
        return redirect('register')

    if request.method == 'POST':
        selected_ids = request.POST.get('selected_subsubjects_ids', '[]')
        selected_ids_list = json.loads(selected_ids)
        request.user.subsubjects.clear()
        for sid in selected_ids_list:
            sub_obj = Subsubject.objects.get(id=sid)
            request.user.subsubjects.add(sub_obj)
        request.user.save()
        return redirect('select_time')

    subjects = Subject.objects.all()
    return render(request, 'main_page/select_subject.html', {
        'subjects': subjects
    })


def profile_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Not authenticated"}, status=401)
    user = request.user
    data = {
        "email": user.email,
        "nickname": user.nickname,
        "role": user.role,
        "city": user.city,
        "info": user.info,
        "teachers": [],
        "friends": [],
        "subjects": list(user.subsubjects.values_list('ss_name', flat=True))
    }
    return JsonResponse(data)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Невірні email або пароль")
            return redirect('user_login')
    return render(request, 'main_page/login.html')

def select_time(request):
    if not request.user.is_authenticated:
        return redirect('register')

    if request.method == 'POST':
        selected_times = request.POST.getlist('times')  # або JSON
        request.user.available_times = selected_times
        request.user.save()
        return redirect('final_step')

    context = {
        'hours': list(range(0, 25)),
        'days': ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    }
    return render(request, 'main_page/select_time.html', context)


def final_step(request):
    user_choice = request.session.get('user_choice')
    if not user_choice:
        return redirect('index')

    if not request.user.is_authenticated:
        return redirect('register')

    if user_choice == "find_friends":
        return redirect('find_friends_final')
    elif user_choice == "find_tutor_indiv":
        return redirect('tutor_indiv_final')
    elif user_choice == "find_tutor_group":
        return redirect('tutor_group_final')
    elif user_choice == "become_tutor":
        return redirect('profile')
    else:
        return redirect('index')


def profile(request):
    return render(request, 'main_page/profile.html')

def find_friends_final(request):
    """
    Шукає друзів (role='learner') з перетином підпредметів/часу.
    """
    # Витягаємо з бази обрані user.subsubjects і user.available_times
    selected_subsubjects = list(request.user.subsubjects.values_list('ss_name', flat=True))
    chosen_times = request.user.available_times or []

    recommended_friends = find_recommended_users(
        role='learner',
        selected_subsubjects=selected_subsubjects,
        chosen_times=chosen_times,
        exclude_user_id=request.user.id
    )
    return render(request, 'main_page/find_friends_final.html', {
        'recommended_friends': recommended_friends
    })



def tutor_indiv_final(request):
    """
    Шукає репетиторів (role='teacher') з перетином підпредметів/часу.
    """
    selected_subsubjects = list(request.user.subsubjects.values_list('ss_name', flat=True))
    chosen_times = request.user.available_times or []

    recommended_tutors = find_recommended_users(
        role='teacher',
        selected_subsubjects=selected_subsubjects,
        chosen_times=chosen_times,
        exclude_user_id=request.user.id
    )
    return render(request, 'main_page/tutor_indiv_final.html', {
        'recommended_tutors': recommended_tutors
    })


def tutor_group_final(request):
    """
    Шукає репетиторів (role='teacher', group_teaching=True) з перетином підпредметів/часу.
    """
    selected_subsubjects = list(request.user.subsubjects.values_list('ss_name', flat=True))
    chosen_times = request.user.available_times or []

    qs = User.objects.filter(role='teacher', group_teaching=True).exclude(id=request.user.id)

    recommended_tutors = []
    for user in qs:
        user_subs = list(user.subsubjects.values_list('ss_name', flat=True))
        user_times = user.available_times or []

        overlap_subs = set(selected_subsubjects).intersection(user_subs)
        overlap_times = set(chosen_times).intersection(user_times)

        if overlap_subs or overlap_times:
            recommended_tutors.append(user)

    return render(request, 'main_page/tutor_group_final.html', {
        'recommended_tutors': recommended_tutors
    })


def find_recommended_users(role, selected_subsubjects, chosen_times, exclude_user_id):
    """
    Повертає список користувачів із потрібною роллю (learner/teacher),
    у яких є перетин підпредметів (user.subsubjects) або тайм-слотів (user.available_times).
    """
    qs = User.objects.filter(role=role).exclude(id=exclude_user_id)

    recommended = []
    for user in qs:
        user_subs = list(user.subsubjects.values_list('ss_name', flat=True))
        user_times = user.available_times or []

        # Перетини
        overlap_subs = set(selected_subsubjects).intersection(user_subs)
        overlap_times = set(chosen_times).intersection(user_times)

        if overlap_subs or overlap_times:
            recommended.append(user)

    return recommended


def user_logout(request):
    logout(request)
    return redirect('index')

def subject_pie_chart(request):
    subject_counts = {}
    all_subjects = Subject.objects.all()
    for subj in all_subjects:
        # Отримуємо ID всіх підпредметів цього предмета
        sub_ids = subj.subsubject_set.values_list('id', flat=True)
        # Рахуємо користувачів, які мають хоч один із цих підпредметів
        count_users = User.objects.filter(subsubjects__in=sub_ids).distinct().count()
        if count_users > 0:
            subject_counts[subj.sb_name] = count_users

    labels = list(subject_counts.keys())
    sizes = list(subject_counts.values())

    # Якщо взагалі немає предметів із >0 користувачами,
    # можна показати порожню діаграму або повернути зображення з текстом.
    if len(sizes) == 0:
        # Згенеруємо простий текст-діаграму
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Ніхто не обрав жодного предмета", ha='center', va='center')
        ax.axis('off')
    else:
        # Малюємо звичайну діаграму
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # кругова діаграма

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')
