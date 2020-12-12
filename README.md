### Todos
- Config boto3, aws key + aws credential
- tạo một templates có upload form
- tạo một view function để handle request từ template, fileview function này sẽ connect tới S3 bằng boto3 để upload file
- tạo 1 bucket trên s3 để chứa file
- khi user upload 1 file từ upload form thì file sẽ chuyern thành binary gởi vào view function. function thực hiên upload lên s3. upload thành công thì hiện thông báo success, fail thì báo lỗi
- tạo presigned url để  lấy src nhúng vào thẻ input

## Setup
Clone project
* cd Aws3_Boto3
* pip install -r requirements.txt
* source v/bin/activate
* python manage.py runserver

## Link

* default : http://127.0.0.1:8000
* search bucket: http://127.0.0.1:8000/search_bucket/  tìm bucket và trả về danh sách các ảnh trong thư mục đó

## Contact
Created by Nam Trần