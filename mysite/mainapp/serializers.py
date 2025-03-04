# mainapp/serializers.py

from rest_framework import serializers
from .models import (
    User, Subject, Subsubject, StudyProgram,
    LearnersSubsubjects, TeachersSubsubjects,
    FriendsByLearner, LearnersPerTeachers
)

# -----------------------------
# 1) Базовий серіалізатор користувача
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    subsubjects = serializers.PrimaryKeyRelatedField(many=True, queryset=Subsubject.objects.all(), required=False)
    available_times = serializers.JSONField(default=list, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'nickname', 'role',
            'city', 'info', 'social_networks',
            'available_times', 'subsubjects'
        ]

# -----------------------------
# 2) Розширений серіалізатор профілю
# -----------------------------
class ProfileSerializer(UserSerializer):
    """
    Наслідуємо поля з UserSerializer,
    + додаємо поля friends і teachers (тільки для читання).
    """
    teachers = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['teachers', 'friends']
        # Тобто беремо всі поля з UserSerializer + додаємо два нові

    def get_teachers(self, obj):
        """
        Повертає список викладачів поточного користувача (якщо user - учень).
        У моделі LearnersPerTeachers є поле "learner" -> "teachers" (related_name).
        """
        # Оскільки в моделі:
        # class LearnersPerTeachers(models.Model):
        #     learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teachers")
        #     teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students")
        #
        # То obj.teachers.all() дає нам усі зв’язки, де learner = obj.
        teacher_links = obj.teachers.all()
        return [
            {
                'id': link.teacher.id,
                'nickname': link.teacher.nickname
            }
            for link in teacher_links
        ]

    def get_friends(self, obj):
        """
        Повертає список друзів.
        Користувач може бути в friend1 або friend2 (related_name="friend1"/"friend2").
        """
        from django.db.models import Q

        # Всі зв’язки, де obj є в полі fl_learner_id_1
        friend_links_1 = obj.friend1.all()
        # Всі зв’язки, де obj є в полі fl_learner_id_2
        friend_links_2 = obj.friend2.all()

        friend_links = list(friend_links_1) + list(friend_links_2)
        friends_list = []

        for link in friend_links:
            if link.fl_learner_id_1 == obj:
                friend_user = link.fl_learner_id_2
            else:
                friend_user = link.fl_learner_id_1

            friends_list.append({
                'id': friend_user.id,
                'nickname': friend_user.nickname
            })

        return friends_list


# -----------------------------
# (Решта серіалізаторів - без змін)
# -----------------------------
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubsubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsubject
        fields = '__all__'

class StudyProgramSerializer(serializers.ModelSerializer):
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = StudyProgram
        fields = '__all__'

class LearnersSubsubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnersSubsubjects
        fields = '__all__'

class TeachersSubsubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachersSubsubjects
        fields = '__all__'
