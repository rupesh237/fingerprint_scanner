from django import forms
from .models import DocumentUpload

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ['name', 'document_type', 'document_file']

