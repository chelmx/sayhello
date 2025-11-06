from wtforms.validators import ValidationError

class ColorValidator(object):
    def __call__(self, form, field):
        if not field.data or isinstance(field.data, (str, )) and not field.data.strip():
            value = field.data
            if not (value.startswith('#') and len(value) == 7 and all(c in '0123456789ABCDEFabcdef' for c in value[1:])):
                raise ValidationError("Color is invalid")