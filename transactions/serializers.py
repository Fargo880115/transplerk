# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import Company, Transaction, SystemUser


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
        model = SystemUser
