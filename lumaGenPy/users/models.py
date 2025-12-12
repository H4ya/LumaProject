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
    
class RealWorldMagic(models.Model):
    
    magic_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        'Topic', 
        on_delete=models.CASCADE,
        db_column='topic_id',
        related_name='real_world_magic_points'
    )
    
    icon = models.CharField(max_length=50, blank=True, null=True)
    card_title = models.CharField(max_length=255)
    card_description = models.TextField()

    class Meta:
        verbose_name = "Real-World Magic Point"
        verbose_name_plural = "Real-World Magic Points"
        managed = False
        db_table = 'real_world_magic' 

    def __str__(self):
        return f"{self.topic.title} - {self.card_title}"



class LearningUnlock(models.Model):

    unlock_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        'Topic', 
        on_delete=models.CASCADE,
        db_column='topic_id',
        related_name='learning_unlocks'
    )
    
    list_item = models.TextField()

    class Meta:
        verbose_name = "Learning Unlock Item"
        verbose_name_plural = "Learning Unlock Items"
        
        managed = False
        db_table = 'learning_unlocks' 

    def __str__(self):
        return f"Unlock for {self.topic.title}"

class ExternalResource(models.Model):

    resource_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(
        'Topic', 
        on_delete=models.CASCADE,
        db_column='topic_id',
        related_name='external_resources'
    )
    
    icon = models.CharField(max_length=50, blank=True, null=True)
    link_title = models.CharField(max_length=255)
    url = models.TextField()

    class Meta:
        verbose_name = "External Resource"
        verbose_name_plural = "External Resources"
        managed = False
        db_table = 'external_resources' 

    def __str__(self):
        return f"Resource for {self.topic.title} - {self.link_title}"



class Topic(models.Model):
    
    topic_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    subtitle = models.CharField(max_length=255, blank=True, null=True) 
    purpose = models.TextField(blank=True, null=True)
    why_it_matters = models.TextField(blank=True, null=True)
    mini_story = models.TextField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)

    
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Draft'
    )
    
    
    last_modified = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(
        'Admins',
        on_delete=models.CASCADE,
        related_name='created_topics'
    )

    class Meta:
        managed = False
        db_table = 'topics'
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering = ['title']

    def __str__(self):
        return self.title




# Start of edit wesam - Save model
class Save(models.Model):
    std_id = models.IntegerField(primary_key=True)
    topic_id = models.IntegerField()

    class Meta:
        unique_together = (('std_id', 'topic_id'),)
        db_table = 'saves'
        managed = False

    def __str__(self):
        return f"Student {self.std_id} saved topic {self.topic_id}"

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

