# -*- coding: utf-8 -*-

from django import forms


class DocumentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        n = kwargs.pop('n')
        super(DocumentForm, self).__init__(*args, **kwargs)
        for i in range(0, n):
            self.fields['Lower Bound %s' % (i+1)] = forms.DecimalField()
            self.fields['Upper Bound %s' % (i + 1)] = forms.DecimalField()
            self.fields['Step %s' % (i + 1)] = forms.DecimalField()
    # lower = forms.DecimalField(
    #     label="Select lower bound for threshold"
    # )
    # upper = forms.DecimalField(
    #     label="Select upper bound for threshold"
    # )
    # step = forms.DecimalField(
    #     label="Select step for threshold"
    # )


class FileForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )


