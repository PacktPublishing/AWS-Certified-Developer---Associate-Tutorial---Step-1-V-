from django.shortcuts import render
from .forms import FilesForm
from django.http import HttpResponseRedirect
from .upload_to_s3 import connect_to_s3_resource, upload_to_bucket, connect_to_s3_client, s3_object_meta, retrieve_objects_from_s3
from django.conf import settings

def home(request):
    return render(request, 'home.html', {})

def upload(request):
    if request.method == 'POST':
        form = FilesForm(request.POST, request.FILES)
        if form.is_valid():
            new_image_details = request.FILES.get('image_file')
            image_file = form.fields.get('image_file')
            description = form.cleaned_data['image_description']
            s3 = connect_to_s3_resource(settings.AWS_REGION_NAME)
            upload_to_bucket(str(new_image_details.name), new_image_details, s3, settings.AWS_BUCKET_NAME, ExtraArgs={'Metadata': {'description': description}, 'ACL':'public-read'})
            return HttpResponseRedirect('/successful')
    else:
        form = FilesForm()
    context = {'layout': 'vertical', 'form': form}
    return render(request, 'upload.html', context)

def successful(request):
    return render(request, 'successful.html')

def view(request):
    client = connect_to_s3_client(settings.AWS_REGION_NAME)
    context = {'all_items':retrieve_objects_from_s3(client,settings.AWS_BUCKET_NAME),
                'bucket_url': settings.AWS_BUCKET_URL}
    return render(request, 'viewall.html', context)
