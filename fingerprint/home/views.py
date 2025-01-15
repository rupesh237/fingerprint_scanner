from django.shortcuts import render

# Create your views here.
import cv2
from django.shortcuts import render, redirect
from .models import Fingerprint
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import numpy as np
import base64
from io import BytesIO
from PIL import Image

def scan_fingerprint(request):
    if request.method == "POST":
        name = request.POST.get("name")
        # Access the webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return render(request, 'home/scan_fingerprint.html', {'error': 'Unable to access the camera'})

        # Capture one frame
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return render(request, 'home/scan_fingerprint.html', {'error': 'Failed to capture image'})

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Save the fingerprint as an image file
        success, encoded_image = cv2.imencode('.jpg', gray_frame)
        if not success:
            return render(request, 'home/scan_fingerprint.html', {'error': 'Failed to encode image'})

        fingerprint_data = encoded_image.tobytes()
        file_name = f'fingerprint_{name}.jpg'

        # Save the file to the Django storage
        path = default_storage.save(f'fingerprints/{file_name}', ContentFile(fingerprint_data))

        # Save to the database
        Fingerprint.objects.create(name=name, fingerprint_image=path)

        return redirect('fingerprint_success')

    return render(request, 'home/scan_fingerprint.html')

def fingerprint_success(request):
    return render(request, 'home/fingerprint_success.html')