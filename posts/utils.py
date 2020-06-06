from django.utils.text import slugify


def custom_slugify(text):
    dot_converted_text = text.upper().replace(".", "-")
    return slugify(dot_converted_text, allow_unicode=False).strip("-")


def upload_to():
    pass


