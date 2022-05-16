# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import render

# Create your views here.


class Resume(APIView):

    def get(self):
        """
        Get the resume of database information
        """
        from .models import Company, Transaction
        from .serializers import CompanySerializer
        try:
            # get more selling company
            more_sells_company = Company.objects.more_sells_company()
            # get less selling company
            less_sells_company = Company.objects.less_sells_company()
            # get more rejected company
            more_rejected_company = Company.objects.more_rejected_sells_company()
            # total price purchased
            total_price_purchased = Transaction.objects.total_price_approved()
            # total prices don't purchased
            total_price_not_purchased = Transaction.objects.total_price_not_approved()

            return Response({
                'more_sells_company': CompanySerializer(more_sells_company).data,
                'less_sells_company': CompanySerializer(less_sells_company).data,
                'more_rejected_company': CompanySerializer(more_rejected_company).data,
                'total_price_purchased': total_price_purchased,
                'total_price_not_purchased': total_price_not_purchased
            })
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


resume = Resume.as_view()


class Company(APIView):

    def get(self, company_id):
        """
        Get company information
        """
        from .models import Company, Transaction
        from .serializers import CompanySerializer
        try:
            try:
                company = get_object_or_404(Company, id=company_id)
            except ValueError:
                from django.http import Http404
                raise Http404

            # total transaction approved
            total_transaction_approved = Transaction.objects.total_transactions_approved(company)
            # total transactions don't approved
            total_transaction_not_approved = Transaction.objects.total_transactions_not_approved(company)
            # get more selling date for company
            more_sells_date = Transaction.objects.more_sells_date(company)

            return Response({
                'company': CompanySerializer(company).data,
                'total_transaction_approved': total_transaction_approved,
                'total_transaction_not_approved': total_transaction_not_approved,
                'more_sells_date': more_sells_date
            })
        except Http404 as ex:
            return Response({'error': str(ex)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


company = Company.as_view()

