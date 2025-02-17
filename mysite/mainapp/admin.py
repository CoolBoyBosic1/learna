from django.contrib import admin
from .models import Learner, Teacher, FriendsByLearner, StudyProgram, Subject, Subsubject, LearnersPerTeachers, TeachersPerStudyPrograms, LearnersSubsubjects, TeachersSubsubjects

admin.site.register(Learner)
admin.site.register(Teacher)
admin.site.register(FriendsByLearner)
admin.site.register(StudyProgram)
admin.site.register(Subject)
admin.site.register(Subsubject)
admin.site.register(LearnersPerTeachers)
admin.site.register(TeachersPerStudyPrograms)
admin.site.register(LearnersSubsubjects)
admin.site.register(TeachersSubsubjects)
