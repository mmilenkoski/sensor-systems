# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import document, fileupload, parameters, results, hello

urlpatterns = [
    url(r'^list/$', document, name='list'),
    url(r'^hello/$', hello, name='hello'),
    url(r'^fileupload/$', fileupload, name='file'),
    url(r'^parameters/$', parameters, name='parameters'),
    url(r'^results/$', results, name='results')
]
