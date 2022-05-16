# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Company, Transaction
from .serializers import CompanySerializer, TransactionSerializer
from django.shortcuts import render

# Create your views here.


class Companies(APIView):

    def get(self, request):
        """
        Get companies information. 'status' query param add this filter
        """
        try:
            req_status = request.query_params.get('status', '')

            target_companies = Company.objects.all().exclude(deleted=True)

            if req_status:
                target_companies = target_companies.filter(status=req_status)

            return Response(CompanySerializer(target_companies, many=True).data)
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


companies = Companies.as_view()


class CompanyTransactions(APIView):

    def get(self, request, company_id):
        """
        Get all transactions associated to a given company
        """
        try:
            try:
                existing_company = get_object_or_404(Company, id=company_id)
                if existing_company.deleted:
                    raise Http404
            except ValueError:
                raise Http404

            target_transactions = Transaction.objects.filter(company=existing_company).exclude(deleted=True)

            return Response(TransactionSerializer(target_transactions, many=True).data)
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


company_transactions = CompanyTransactions.as_view()


class Resume(APIView):

    def get(self, request):
        """
        Get the resume of database information
        """
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

    def get(self, request, company_id):
        """
        Get company information
        """
        try:
            try:
                existing_company = get_object_or_404(Company, id=company_id)
                if existing_company.deleted:
                    raise Http404
            except ValueError:
                raise Http404

            # total transaction approved
            total_transaction_approved = Transaction.objects.total_transactions_approved(existing_company)
            # total transactions don't approved
            total_transaction_not_approved = Transaction.objects.total_transactions_not_approved(existing_company)
            # get more selling date for company
            more_sells_date = Transaction.objects.more_sells_date(existing_company)

            return Response({
                'company': CompanySerializer(existing_company).data,
                'total_transaction_approved': total_transaction_approved,
                'total_transaction_not_approved': total_transaction_not_approved,
                'more_sells_date': more_sells_date
            })
        except Http404 as ex:
            return Response({'error': str(ex)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


company = Company.as_view()

