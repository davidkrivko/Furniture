import os.path
import uuid

from django.utils.text import slugify


def image_file_path(instance, file_name):
    _, extension = os.path.splitext(file_name)

    file_name = f"{slugify(instance.info)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/furniture", file_name)
