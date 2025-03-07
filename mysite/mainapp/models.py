from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models



# ====== Предмети ======
class Subject(models.Model):
    CATEGORY_CHOICES = [
        ('Programming', 'Програмування'),
        ('Math', 'Математика'),
        ('Languages', 'Мови')
    ]

    sb_name = models.CharField(max_length=100, unique=True, verbose_name="Назва предмета")
    sb_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категорія")

    def __str__(self):
        return self.sb_name


# ====== Підтематики ======
class Subsubject(models.Model):
    objects = None
    ss_name = models.CharField(max_length=100, unique=True, verbose_name="Назва підпредмета")
    sb_id = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")

    def __str__(self):
        return self.ss_name



# Менеджер користувачів
class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError("Користувач повинен мати email")
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("learner", "Учень"),
        ("teacher", "Вчитель"),
        ("admin", "Адміністратор"),
    ]

    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="learner")
    city = models.CharField(max_length=50, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    social_networks = models.TextField(null=True, blank=True)
    available_times = models.JSONField(default=list, blank=True)  # Доступні слоти
    subsubjects = models.ManyToManyField(Subsubject, related_name="users", blank=True)  # Додаємо зв’язок

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.nickname



# ====== Друзі учнів ======
class FriendsByLearner(models.Model):
    fl_learner_id_1 = models.ForeignKey(User, related_name="friend1", on_delete=models.CASCADE)
    fl_learner_id_2 = models.ForeignKey(User, related_name="friend2", on_delete=models.CASCADE)
    fl_time_found = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('fl_learner_id_1', 'fl_learner_id_2')

# ====== Навчальні програми ======
class StudyProgram(models.Model):
    FORMAT_CHOICES = [
        ('individual', 'Індивідуальне навчання'),
        ('group', 'Групове навчання')
    ]

    st_start_date = models.DateField(verbose_name="Дата початку")
    st_end_date = models.DateField(verbose_name="Дата завершення")
    st_format = models.CharField(max_length=50, choices=FORMAT_CHOICES, verbose_name="Формат")
    st_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    students = models.ManyToManyField(User, related_name="study_programs", limit_choices_to={'role': 'learner'})

    def __str__(self):
        return f"{self.st_subject} ({self.st_format})"


# ====== Співвідношення викладачів та учнів ======
class LearnersPerTeachers(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teachers")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students")

    class Meta:
        unique_together = ('learner', 'teacher')


# ====== Співвідношення викладачів та навчальних програм ======
class TeachersPerStudyPrograms(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    study_program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE)


# ====== Співвідношення учнів та підтем ======
class LearnersSubsubjects(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'learner'})
    subsubject = models.ForeignKey(Subsubject, on_delete=models.CASCADE)


# ====== Співвідношення викладачів та підтем ======
class TeachersSubsubjects(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    subsubject = models.ForeignKey(Subsubject, on_delete=models.CASCADE)
