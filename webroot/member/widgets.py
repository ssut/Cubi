from django import forms

class SplitInputWidget(forms.MultiWidget):
    def __init__(self, number, each_attrs=None, attrs=None):
        self.item_number = int(number)
        widgets = []
        for i in range(number):
            try:
                cur_attrs = each_attrs[i]
                if 'password-field' in cur_attrs:
                    widget = forms.PasswordInput(attrs=cur_attrs)
                else:
                    widget = forms.TextInput(attrs=cur_attrs)
            except:
                if 'password-field' in attrs:
                    widget = forms.PasswordInput(attrs=attrs)
                else:
                    widget = forms.TextInput(attrs=attrs)
            widgets.append(widget)
        super(SplitInputWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split('-')
        else:
            return [None]

    def format_output(self, rendered_widgets):
        return u'  -  '.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        value_list = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)
        ]
        return_str = ''
        for i in range(self.item_number):
            return_str += str(value_list[i])
            if i != self.item_number-1:
                return_str += '-'

        return return_str
