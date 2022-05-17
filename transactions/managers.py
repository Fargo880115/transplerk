# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Sum, Count


class CompanyManager(models.Manager):
    def more_sells_company(self):
        """
        Get company with more sells
        :return:
        """
        try:
            more_sells_company = self.filter(transactions__final_payment=True).annotate(num_trans=Count('transactions')).order_by('num_trans').last()
            return more_sells_company
        except Exception as ex:
            raise

    def less_sells_company(self):
        """
        Get company with less sells
        :return:
        """
        try:
            less_sells_company = self.filter(transactions__final_payment=True).annotate(
                num_trans=Count('transactions')).order_by('num_trans').first()
            return less_sells_company
        except Exception as ex:
            raise

    def more_rejected_sells_company(self):
        """
        Get company with more rejected sells
        :return:
        """
        try:
            rejected_sells_company = self.filter(transactions__final_payment=False).annotate(
                num_trans=Count('transactions')).order_by('num_trans').last()
            return rejected_sells_company
        except Exception as ex:
            raise


class TransactionManager(models.Manager):

    def more_sells_date(self, company):
        """
        Get date with more sells
        :return:
        """
        try:
            transaction_date_list = self.filter(company=company, final_payment=True, deleted=False).extra(
                {'trans_date': "date(transaction_date)"}).values('trans_date').annotate(total_count=Count('id')).order_by('total_count').last()
            return transaction_date_list
        except Exception as ex:
            raise

    def total_price_approved(self):
        """
        Get total price for approved transactions
        :return:
        """
        try:
            return self.filter(final_payment=True).exclude(deleted=True).aggregate(Sum('price'))['price__sum']
        except Exception as ex:
            raise

    def total_price_not_approved(self):
        """
        Get total price for non approved transactions
        :return:
        """
        try:
            return self.filter(final_payment=False).exclude(deleted=True).aggregate(Sum('price'))['price__sum']
        except Exception as ex:
            raise

    def transaction_count(self, company):
        """
        Get transactions count for a given company
        :return:
        """
        try:
            return self.filter(company=company, final_payment=True).exclude(deleted=True).count() if company else 0
        except Exception as ex:
            raise

    def rejected_transaction_count(self, company):
        """
        Get rejected transactions count for a given company
        :return:
        """
        try:
            return self.filter(company=company, final_payment=False).exclude(deleted=True).count() if company else 0
        except Exception as ex:
            raise

    def total_transactions_approved(self, company):
        """
        Get total transaction approved for given company
        :return:
        """
        try:
            return self.filter(company=company, final_payment=True).exclude(deleted=True).count()
        except Exception as ex:
            raise

    def total_transactions_not_approved(self, company):
        """
        Get total transaction not approved for given company
        :return:
        """
        try:
            return self.filter(company=company, final_payment=False).exclude(deleted=True).count()
        except Exception as ex:
            raise


class SystemUserManager(models.Manager):
    """
    Manger for SystemUser
    """
    pass
