import os
import uuid
from django.utils.text import slugify

from airport_service.settings import MEDIA_ROOT

UPLOAD_FOLDER = os.path.join(MEDIA_ROOT, "uploads/crew/")


def crew_image_file_path(instance, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.last_name)}-{uuid.uuid4()}{extension}"

    return os.path.join(UPLOAD_FOLDER, filename)
