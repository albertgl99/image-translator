from django.db import models

class Translation(models.Model):
    image = models.ImageField(upload_to="uploads/")
    extracted_text = models.TextField()
    translated_text = models.TextField()
    target_language = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
