from rest_framework.serializers import ValidationError


class UrlValidator:
    """Валидатор проверяющий поле ссылки на урок."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = value.get(self.field, "")
        if not tmp_val:
            return
        if not (
            tmp_val.startswith("https://www.youtube.com/")
            or tmp_val.startswith("http://www.youtube.com/")
            or tmp_val.startswith("https://youtube.com/")
            or tmp_val.startswith("http://youtube.com/")
            or tmp_val.startswith("https://youtu.be/")
            or tmp_val.startswith("http://youtu.be/")
        ):
            raise ValidationError(
                "Ссылка недействительна. Разрешены только ссылки на youtube.com."
            )
