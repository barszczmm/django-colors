from colors.validators import hex_color_code_validator
from colors.widgets import ColorPickerWidget
from django.conf import settings
from django.db import models

if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules((), ["^colors\.fields\.ColorField"])


class ColorField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super(ColorField, self).__init__(*args, **kwargs)
        self.validators.append(hex_color_code_validator)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super(ColorField, self).formfield(**kwargs)

