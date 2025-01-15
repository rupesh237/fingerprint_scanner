from django.db import models


class Fingerprint(models.Model):
    name = models.CharField(max_length=255)
    fingerprint_image = models.ImageField(upload_to='fingerprints/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
