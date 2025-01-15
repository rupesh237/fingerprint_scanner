import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Fingerprint
import base64
from .forms import DocumentUploadForm

def scan_fingerprint(request):
    if request.method == "POST":
        name = request.POST.get("name")
        capture_image = request.POST.get("capture_image")

        # Save the captured image
        if capture_image:
            # Decode base64 image string from the hidden input field
            image_data = capture_image.split(",")[1]
            image_bytes = ContentFile(base64.b64decode(image_data))

            # Optimize image size and save
            file_name = f'fingerprint_{name}.jpg'
            fingerprint_path = f'fingerprints/{file_name}'

            # Convert the image bytes to a numpy array for resizing
            nparr = np.frombuffer(image_bytes.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

            # Resize the image to reduce size (e.g., 50% of original size)
            resized_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

            # Re-encode the resized image with lower quality
            success, encoded_img = cv2.imencode('.jpg', resized_img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

            if success:
                # Save the optimized image
                default_storage.save(fingerprint_path, ContentFile(encoded_img.tobytes()))

                # Save record in the database
                Fingerprint.objects.create(name=name, fingerprint_image=fingerprint_path)

                return redirect('fingerprint_success')

        return render(request, 'home/scan_fingerprint.html', {'error': 'Failed to save the image'})

    return render(request, 'home/scan_fingerprint.html')



def fingerprint_success(request):
    return render(request, 'home/fingerprint_success.html')

def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_success')
    else:
        form = DocumentUploadForm()
    return render(request, 'home/upload_document.html', {'form': form})

def document_success(request):
    return render(request, 'home/document_success.html')