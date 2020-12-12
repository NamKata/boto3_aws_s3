
from django.views.generic.edit import FormView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
import boto3
import uuid
import os
from Main import settings
from django.core.files.storage import FileSystemStorage
from .utils import handle_check_exists_bucket, handle_create_bucket_request, \
    handle_upload_mutiplefile_in_bucket, handle_check_is_empty, handle_presigned_url, \
    handle_download_file_s3, handle_presigned_url_set_timeout, \
    handle_rename_file_in_bucket_s3, handle_move_file_in_bucket_s3, \
    handle_list_bucket
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def search_bucket(request):
    if request.method == "POST":
        bucket = request.POST['search']
        if handle_check_exists_bucket(bucket) == True:
            return redirect('list', bucket)
        else:
            return render(request, 'search_bucket.html', {'message':True})
    else:
        return render(request, 'search_bucket.html')
def list_image(request, bucket):
    result = {
        'Success':False,
        'message':''
    }
    # -- generate presigned url
    pre_sign = handle_presigned_url_set_timeout(bucket)
    print(pre_sign)
    if pre_sign is None:
        return Response(result, status= status.HTTP_400_BAD_REQUEST)
    else:
        result['Success'] = True 
        result['message']=''
        # -- generate presinged url set time out
        result['data']={
            'urlimages':pre_sign,
            'bucket':bucket
        }

        return render(request, 'listImages.html', result)


def upload_in_request(request):
    # Config boto3, aws key+ aws credentital -> done
    # Create a templates have upload form -> done
    # Create view function  -> done
    # Create handle request from templates
    # Create a bucket can contain files
    # When user upload file from template response the file to binary file send to view function, function upload to s3
    # Upload then return Success or 
    if request.method == "POST":
        bucketname = request.POST['bucket']
        files = request.FILES.getlist('files')
        if handle_check_is_empty(files, bucketname) == False:
            return render(request,'upload.html', {'message':"Empty!"})

        if handle_upload_mutiplefile_in_bucket(files, bucketname.lower()) == True:
            return render(request,'upload.html', {'message':"Success!"})
        else:
            return render(request,'upload.html', {'message':"Faluire!"})
    else:
        return render(request,'upload.html')


@api_view(['POST'])
def list_url_demo(request):
    result = {
        'Success':False,
        'message':''
    }
    bucket = request.POST['bucket']
    pre_sign= handle_presigned_url_set_timeout(bucket)
    print(pre_sign)
    # return Response(pre_sign)
    if pre_sign is None:
        return Response(result, status= status.HTTP_400_BAD_REQUEST)
    else:
        result['Success'] = True
        result['message']=''
        result['data']= {
            'urlimages':pre_sign,
            'bucket':bucket,
            'presigned':pre_sign
        }
        return Response(result, status = status.HTTP_200_OK)

def download_file(request, bucket):
    if handle_download_file_s3(bucket) == True:
        return redirect('test')
    return redirect('list', bucket)

@api_view(['POST'])
def rename_file(request):
    keyOld = request.POST['keyOld']
    newNameKeyOld = request.POST['newName']
    bucket = request.POST['bucket']
    result = {
        "Success":False,
        "message":"Error!!"
    }
    if handle_rename_file_in_bucket_s3(bucket,keyOld,newNameKeyOld) == True:
        result['Success'] = True
        result['message'] = 'Rename file is success!!'
        return Response(result, status= status.HTTP_202_ACCEPTED)
    return Response(result, status= status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def move_file(request):
    key_file = request.POST['key']
    bucket_1 = request.POST['bucket']
    bucket_2 = request.POST['bucket_move']
    result = {
        "Success":False,
        "message":"Error!!"
    }
    if handle_move_file_in_bucket_s3(bucket_1, bucket_2, key_file) == True:
        result['Success'] = True
        result['message'] = 'Move file is success!!'
        return Response(result, status= status.HTTP_202_ACCEPTED)
    return Response(result, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_bucket(request):
    data ={
        'success':False,
        'message':''
    }
    response = handle_list_bucket()
    return Response(response, status= status.HTTP_200_OK)