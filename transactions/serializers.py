# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Company, Transaction


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ('id',)


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        exclude = ('id', 'creation_date', 'deleted',)


class SystemUserLogInSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'id',)
