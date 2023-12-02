import os
from datetime import datetime, timedelta

from google.cloud import storage

from models import Image

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ageless-webbing-405115-dfeddeb7c47c.json"

bucket_storage = 'cloud_image_bucket'


# uploads file based on local file path, and cloudpath(should be username+filename) -> returns link that lasts one day
def upload_file_to_bucket(bucket_name, file, destination_file_name) -> str:
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    print(file,destination_file_name)

    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(file)

    return blob.generate_signed_url(datetime.today() + timedelta(1))


def get_signed_url(bucket_name, file_name, expire_in=datetime.today() + timedelta(1)):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    url = bucket.blob(file_name).generate_signed_url(expire_in)

    return url


def list_files_of_user(bucket_name, user=""):
    storage_client = storage.Client()
    if user != "":
        user = user + "/"

    file_list = storage_client.list_blobs(bucket_name, prefix=user)
    file_list = [file.name for file in file_list]

    return file_list


# print(get_signed_url(bucket_storage,'imageuser'))
# print(upload_file_to_bucket(bucket_storage, 'temp/test.jpg', '1/image2.jpg'))


def get_signed_urls_for_user(bucket_name, images: list[Image]) -> list[Image]:
    for image in images:
        image.signed_url = get_signed_url(bucket_name, str(image.folder_id) + "/" + image.name)

    return images

#
# files = (list_files_of_user(bucket_storage))
#
# print(get_signed_urls_for_user(bucket_storage, files))
