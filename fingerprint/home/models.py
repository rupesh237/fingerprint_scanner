from django.db import models


class Fingerprint(models.Model):
    name = models.CharField(max_length=255)
    fingerprint_image = models.ImageField(upload_to='fingerprints/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DocumentUpload(models.Model):
    DOCUMENT_TYPES = [
        ('CITIZENSHIP', 'Citizenship'),
        ('VOTER_ID', 'Voter ID'),
        ('LICENSE', 'License'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=255, help_text="Name of the person associated with the document.")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, help_text="Type of document being uploaded.")
    document_file = models.FileField(upload_to='documents/', help_text="Upload the document file.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_document_type_display()}"