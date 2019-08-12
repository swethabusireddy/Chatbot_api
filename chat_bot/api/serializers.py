__author__ = 'com'
#from rest_framework import serializers
from .models import *
from rbasis.serializers import *

class testSerializer(ShAPISerializer):
    class Meta:
        model = test
        fields = ('url', 'id', 'name',)
