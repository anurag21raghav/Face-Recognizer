from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import boto3
from .models import Image

bucket = "rekognition-warm-up"
KEY = "{{ uploaded_file_url }}"
COLLECTION = Image.objects.all()
sourceFile = 'source.jpg'
targetFile = 'target.jpg'

def search_faces_by_image(bucket, key, collection_id, threshold=80, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.search_faces_by_image(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		CollectionId=collection_id,
		FaceMatchThreshold=threshold,
	)
	return response['FaceMatches']

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        records = search_faces_by_image(BUCKET, uploaded_file_url, COLLECTION)
        return render(request, 'recognizer/output.html', {'records': records})
        return render(request, 'recognizer/index.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'recognizer/index.html')

def output(request):
	client = boto3.client('rekognition')
	response=client.compare_faces(SimilarityThreshold=70,
									SourceImage={'S3Object':
	{'Bucket':bucket, 'Name':sourceFile}},
									TargetImage={'S3Object':
	{'Bucket':bucket, 'Name':targetFile}})

	for faceMatch in response['FaceMatches']:
		position = faceMatch['Face']['BoundingBox']
		confidence = str(faceMatch['Face']['Confidence'])
		print('The face at ' + 
				str(position['Left']) + ' ' + 
				str(position['Top']) + 
				' matches with ' + confidence + '% confidence')