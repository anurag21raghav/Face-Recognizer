from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'recognizer/index.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'recognizer/index.html')