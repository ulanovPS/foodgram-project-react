import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class HexColorValidator(validators.RegexValidator):
    regex = r'#[0-9A-Fa-f]{6}'
    message = _(
        'Введите верное значение поля Цвет.'
        ' Это поле должно соответствовать формату HEX. Пример: #800000 '
    )
    flags = 0
