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
    email = models.CharField(max_length=255, unique=True)  
    password = models.CharField(max_length=128)  

    class Meta:
        managed = False
        db_table = 'users'
    def __str__(self):
        return self.id
    




class Topic(models.Model):
    
    topic_id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=255, null=False)
    summary = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    #text = models.TextField(blank=True, null=True)

    class Meta:
        
        db_table = 'topics' 
        # Use ordering to display the latest topics first
        ordering = ['title'] 

    def __str__(self):
        return self.title


class Save(models.Model):
    std_id = models.IntegerField(primary_key=True)
    topic_id = models.IntegerField()

    class Meta:
        unique_together = (('std_id', 'topic_id'),)
        db_table = 'saves'
        managed = False

    def __str__(self):
        return f"Student {self.std_id} saved topic {self.topic_id}"


# class Like(models.Model):
#     student = models.ForeignKey(Students, on_delete=models.CASCADE,db_column='std_id', related_name='liked_topics')
#     topic = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column='topic_id', related_name='liked_by')

#     class Meta:
#         unique_together = ('student', 'topic')  # Composite primary key
#         db_table = 'likes'

#     def __str__(self):
#         return f"{self.student} liked {self.topic}"
class Like(models.Model):
    std_id = models.IntegerField(primary_key=True)
    topic_id = models.IntegerField()

    class Meta:
        unique_together = (('std_id', 'topic_id'),)
        db_table = 'likes'
        managed = False

    def __str__(self):
        return f"Student {self.std_id} liked topic {self.topic_id}"


class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='std_id', related_name='notes')
    topic_title = models.CharField(max_length=200, db_column='topic_title')
    note_content = models.TextField(db_column='note_content')
    creation_date = models.DateTimeField(null=True, blank=True, db_column='creation_date')

    class Meta:
        db_table = 'notes'
        managed = False
    
