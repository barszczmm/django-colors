# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                '%s%s' % (
                    getattr(settings, 'STATIC_URL', settings.MEDIA_URL),
                    'colors/css/colorpicker.css',
                ),
            )
        }
        js = (
            '%s%s' % (
                getattr(settings, 'STATIC_URL', settings.MEDIA_URL),
                'colors/js/colorpicker.js',
            ),
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(ColorPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs.update({
            'class': ' '.join(
                [attrs.get('class', ''), 'color-picker-input']
            ).strip()
        })
        rendered = super(ColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u"""<script type="text/javascript">(function($){
$(function(){
    var input = $('#id_%(name)s'), color = '%(value)s',
      preview = $('<div class="color-picker-preview"><div style="background-color:#%(value)s"></div></div>').insertAfter(input);
    input.add(preview).ColorPicker({
        color: '%(value)s',
        onSubmit: function(hsb, hex, rgb, el) { input.val(hex); $(el).ColorPickerHide();$(preview).find('div').css('backgroundColor', '#' + hex); },
        onBeforeShow: function () { $(this).ColorPickerSetColor(input.val()); }
    }).bind('keyup', function(){ $(this).ColorPickerSetColor(input.val()); });
});})(django.jQuery);</script>""" % {
            'name': name,
            'value': value or ''
        })
