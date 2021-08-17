from django.db import models

# Create your models here.
class Note(models.Model):
    subject = models.CharField(max_length=200)
    sttText = models.TextField()
    note_description = models.TextField()
    reg_date = models.DateTimeField()
    audio = models.ImageField(upload_to="audio")
    vis_js_nodes = models.TextField()
    vis_js_edges = models.TextField()
