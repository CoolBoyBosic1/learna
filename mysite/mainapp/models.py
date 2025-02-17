from django.db import models

# Учні
class Learner(models.Model):
    le_id = models.AutoField(primary_key=True)
    le_nickname = models.CharField(max_length=50, unique=True)
    le_email = models.EmailField(unique=True)
    le_password = models.CharField(max_length=60)
    le_city = models.CharField(max_length=50, null=True, blank=True)
    le_info = models.TextField(null=True, blank=True)
    le_social_networks = models.TextField(null=True, blank=True)
    le_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.le_nickname


# Вчителі
class Teacher(models.Model):
    tc_id = models.AutoField(primary_key=True)
    tc_nickname = models.CharField(max_length=50, unique=True)
    tc_email = models.EmailField(unique=True)
    tc_password = models.CharField(max_length=60)
    tc_city = models.CharField(max_length=50, null=True, blank=True)
    tc_info = models.TextField(null=True, blank=True)
    tc_social_networks = models.TextField(null=True, blank=True)
    tc_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.tc_nickname


# Друзі учнів
class FriendsByLearner(models.Model):
    fl_id = models.AutoField(primary_key=True)
    fl_learner_id_1 = models.ForeignKey(Learner, related_name="friend1", on_delete=models.CASCADE)
    fl_learner_id_2 = models.ForeignKey(Learner, related_name="friend2", on_delete=models.CASCADE)
    fl_time_found = models.DateTimeField(auto_now_add=True, null=True)



# Програми навчання
class StudyProgram(models.Model):
    st_id = models.AutoField(primary_key=True)
    st_start_date = models.DateField()
    st_end_date = models.DateField()
    st_format = models.CharField(max_length=50)
    st_subject = models.CharField(max_length=50)
    le_id = models.ForeignKey(Learner, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.st_subject} ({self.st_format})"


# Предмети
class Subject(models.Model):
    sb_id = models.AutoField(primary_key=True)
    sb_name = models.CharField(max_length=100)
    sb_category = models.CharField(max_length=50, choices=[
        ('Programming', 'Programming'),
        ('Math', 'Math'),
        ('Languages', 'Languages')
    ])

    def __str__(self):
        return self.sb_name


# Підтематики
class Subsubject(models.Model):
    ss_id = models.AutoField(primary_key=True)
    ss_name = models.CharField(max_length=100)
    sb_id = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.ss_name


# Учні та вчителі (зв’язок many-to-many)
class LearnersPerTeachers(models.Model):
    lt_id = models.AutoField(primary_key=True)
    lt_learners_id = models.ForeignKey(Learner, on_delete=models.CASCADE)
    lt_teachers_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)


# Вчителі та навчальні програми
class TeachersPerStudyPrograms(models.Model):
    tsp_id = models.AutoField(primary_key=True)
    tc_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    st_id = models.ForeignKey(StudyProgram, on_delete=models.CASCADE)


# Учні та підтематики
class LearnersSubsubjects(models.Model):
    lss_id = models.AutoField(primary_key=True)
    le_id = models.ForeignKey(Learner, on_delete=models.CASCADE)
    ss_id = models.ForeignKey(Subsubject, on_delete=models.CASCADE)


# Вчителі та підтематики
class TeachersSubsubjects(models.Model):
    tss_id = models.AutoField(primary_key=True)
    tc_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    ss_id = models.ForeignKey(Subsubject, on_delete=models.CASCADE)
