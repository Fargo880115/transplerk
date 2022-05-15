# -*- encoding: utf-8 -*-
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
