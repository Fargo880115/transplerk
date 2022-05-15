# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from django.shortcuts import render

# Create your views here.


class Resume(APIView):

    def get(self):
        try:
            pass
        except Exception as ex:
            raise


resume = Resume.as_view()
