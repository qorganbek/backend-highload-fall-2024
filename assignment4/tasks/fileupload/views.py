from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import FileUploadForm
from .tasks import process_file
from .models import FileUpload

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            process_file.delay(upload.id)
            return redirect('progress', upload_id=upload.id)
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})


def check_progress(request, upload_id):
    upload = FileUpload.objects.get(id=upload_id)
    return JsonResponse({'status': upload.status})
