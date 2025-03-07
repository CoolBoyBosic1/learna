# mainapp/views.py
import json
from urllib import request

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User





def index(request):
    if request.method == 'POST':
        # 1) Користувач обрав дію (find_friends, find_tutor_indiv, find_tutor_group, become_tutor)
        user_choice = request.POST.get('choice')
        # 2) Зберігаємо вибір у сесії
        request.session['user_choice'] = user_choice

        # 3) Якщо користувач НЕ залогінений -> на реєстрацію
        if not request.user.is_authenticated:
            return redirect('register')
        else:
            # Якщо залогінений -> одразу на вибір підпредметів
            return redirect('select_subject')

    # Якщо GET-запит, просто рендеримо головну
    return render(request, 'main_page/index.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        city = request.POST.get('city')
        info = request.POST.get('info')

        if password1 != password2:
            messages.error(request, "Паролі не співпадають!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Користувач з таким email вже існує!")
            return redirect('register')

        if User.objects.filter(nickname=nickname).exists():
            messages.error(request, "Такий нікнейм вже існує!")
            return redirect('register')

        # Створюємо користувача
        user = User.objects.create_user(
            email=email,
            nickname=nickname,
            password=password1,
            city=city,
            info=info
        )
        login(request, user)
        messages.success(request, "Ви успішно зареєструвалися!")

        # Після успішної реєстрації перевіримо, чи є в сесії user_choice
        user_choice = request.session.get('user_choice')
        if user_choice:
            # Якщо вибір вже є, переходимо до вибору підпредметів
            return redirect('select_subject')
        else:
            # Якщо з якоїсь причини user_choice немає, на головну
            return redirect('index')

    return render(request, 'main_page/register.html')


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

def select_subject(request):
    # Якщо користувач НЕ залогінений, краще знову пересвідчитись, що йде на реєстрацію
    if not request.user.is_authenticated:
        return redirect('register')

    if request.method == 'POST':
        # Зчитаємо JSON-рядок із прихованого поля
        subsubjects_json = request.POST.get('selected_subsubjects', '[]')
        subsubjects_list = json.loads(subsubjects_json)
        request.session['selected_subsubjects'] = subsubjects_list

        # Переходимо до вибору часу
        return redirect('select_time')

    return render(request, 'main_page/select_subject.html')


def select_time(request):
    if not request.user.is_authenticated:
        return redirect('register')  # Якщо ні, перекидаємо на реєстрацію

    if request.method == 'POST':
        selected_times_json = request.POST.get('selected_times', '[]')
        selected_times_list = json.loads(selected_times_json)
        request.session['chosen_times'] = selected_times_list

        # Після вибору часу -> переходимо до фінального кроку
        return redirect('final_step')

    context = {
        'hours': list(range(0, 25)),
        'days': ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    }
    return render(request, 'main_page/select_time.html', context)


def final_step(request):
    # Перевіряємо user_choice
    user_choice = request.session.get('user_choice')
    if not user_choice:
        # Якщо чомусь немає вибору, повертаємо на головну
        return redirect('index')

    # Якщо користувач не залогінений, теж на головну або реєстрацію
    if not request.user.is_authenticated:
        return redirect('register')

    # Тепер залежно від user_choice:
    if user_choice == "find_friends":
        return redirect('find_friends_final')
    elif user_choice == "find_tutor_indiv":
        return redirect('tutor_indiv_final')
    elif user_choice == "find_tutor_group":
        return redirect('tutor_group_final')
    elif user_choice == "become_tutor":
        return redirect('profile')
    else:
        # На всяк випадок
        return redirect('index')


def profile(request):
    return render(request, 'main_page/profile.html')

def find_friends_final(request):
    selected_subsubjects = request.session.get('selected_subsubjects', [])
    chosen_times = request.session.get('chosen_times', [])

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
    selected_subsubjects = request.session.get('selected_subsubjects', [])
    chosen_times = request.session.get('chosen_times', [])

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
    selected_subsubjects = request.session.get('selected_subsubjects', [])
    chosen_times = request.session.get('chosen_times', [])

    # Припустимо, у вас є поле `group_teaching = True/False` у моделі
    qs = User.objects.filter(role='teacher', group_teaching=True).exclude(id=request.user.id)

    recommended_tutors = []
    for user in qs:
        user_subs = [s.ss_name for s in user.subsubjects.all()]
        user_times = user.available_times or []

        overlap_subs = set(selected_subsubjects).intersection(user_subs)
        overlap_times = set(chosen_times).intersection(user_times)

        if overlap_subs or overlap_times:
            recommended_tutors.append(user)

    return render(request, 'main_page/tutor_group_final.html', {
        'recommended_tutors': recommended_tutors
    })


def profile_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Not authenticated"}, status=401)

    # Збираємо дані користувача; якщо потрібно, можна додати логіку для teachers/friends
    data = {
        "email": request.user.email,
        "nickname": request.user.nickname,
        "role": request.user.role,
        "city": request.user.city,
        "info": request.user.info,
        "teachers": [],  # Можна заповнити, якщо є зв’язки з викладачами
        "friends": []  # Можна заповнити, якщо є зв’язки з друзями
    }
    return JsonResponse(data)

def find_recommended_users(role, selected_subsubjects, chosen_times, exclude_user_id):
    """
    Повертає список користувачів із заданою роллю (learner/teacher),
    у яких є перетин підпредметів або тайм-слотів.
    exclude_user_id - користувача, якого треба виключити (наприклад, request.user.id)
    """
    # Отримаємо всіх користувачів із потрібною роллю
    qs = User.objects.filter(role=role).exclude(id=exclude_user_id)

    recommended = []
    for user in qs:
        # Збираємо назви підпредметів юзера (припускаємо, що user.subsubjects - це M2M)
        user_subs = list(user.subsubjects.values_list('ss_name', flat=True))  # Отримуємо лише значення назв
        user_times = user.available_times or []  # Тайм-слоти користувача

        # Переконаємось, що вибрані підпредмети - це список рядків
        selected_subsubjects = [s if isinstance(s, str) else s.get('ss_name', '') for s in selected_subsubjects]
        chosen_times = [t if isinstance(t, str) else str(t) for t in chosen_times]

        # Знаходимо перетини
        overlap_subs = set(selected_subsubjects).intersection(user_subs)
        overlap_times = set(chosen_times).intersection(user_times)

        # Якщо є збіг хоча б в одному параметрі - додаємо в рекомендації
        if overlap_subs or overlap_times:
            recommended.append(user)

    return recommended

def user_logout(request):
    logout(request)
    return redirect('index')