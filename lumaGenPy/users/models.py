from django.db import models
from django.utils import timezone

class Admins(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_password = models.TextField()  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)

    class Meta:
        managed = False  
        db_table = 'admins' 

    def __str__(self):
        return self.email
    
class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_password = models.TextField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'students'

    def __str__(self):
        return self.email  
    
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.CharField(unique=True)  
    password = models.CharField(max_length=128)  

    class Meta:
        managed = False
        db_table = 'users'
    def __str__(self):
        return self.id
    




class Topics(models.Model):
    topic_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'topics' 


class Save(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='std_id', related_name='saved_topics')
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, db_column='topic_id', related_name='saved_by')
    saved_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'topic')
        db_table = 'saves'
        managed = False  # Prevent migrations for this table

    def __str__(self):
        return f"{self.student} saved {self.topic}"


# class Like(models.Model):
#     student = models.ForeignKey(Students, on_delete=models.CASCADE,db_column='std_id', related_name='liked_topics')
#     topic = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column='topic_id', related_name='liked_by')

#     class Meta:
#         unique_together = ('student', 'topic')  # Composite primary key
#         db_table = 'likes'

#     def __str__(self):
#         return f"{self.student} liked {self.topic}"
class Like(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='std_id', related_name='liked_topics')
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, db_column='topic_id', related_name='liked_by')

    class Meta:
        unique_together = ('student', 'topic')
        db_table = 'likes'
        managed = False


class Note(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='std_id', related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_edited = models.DateTimeField(auto_now=True)
    key_takeaway = models.TextField()

    class Meta:
        db_table = 'notes'
        managed = False
    

