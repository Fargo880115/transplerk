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
            # companies = self.all().exclude(deleted=True)
            companies = self.filter(deleted=True)
            # c = companies.annotate(total_sells=Count('transactions__final_payment'))
            more_sells_company = max([{'company': c, 'trans_count': self.sells_count(c)} for c in companies],
                                     key=lambda x: x['trans_count'])
            return more_sells_company['company']
        except Exception as ex:
            raise

    def less_sells_company(self):
        """
        Get company with less sells
        :return:
        """
        try:
            companies = self.all().exclude(deleted=True)
            less_sells_company = min([{'company': c, 'trans_count': self.sells_count(c)} for c in companies],
                                     key=lambda x: x['trans_count'])
            return less_sells_company['company']
        except Exception as ex:
            raise

    def more_rejected_sells_company(self):
        """
        Get company with more rejected sells
        :return:
        """
        try:
            companies = self.all().exclude(deleted=True)
            rejected_sells_company = max([{'company': c, 'rejected_trans_count': self.rejected_sells_count(c)} for c in companies],
                                         key=lambda x: x['rejected_trans_count'])
            return rejected_sells_company['company']
        except Exception as ex:
            raise

    def sells_count(self, company):
        """
        Get company sells count
        :return:
        """
        try:
            from .models import Transaction
            return Transaction.objects.transaction_count(company)
        except Exception as ex:
            raise

    def rejected_sells_count(self, company):
        """
        Get company rejected sells count
        :return:
        """
        try:
            from .models import Transaction
            return Transaction.objects.rejected_transaction_count(company)
        except Exception as ex:
            raise


class TransactionManager(models.Manager):

    def more_sells_date(self, company):
        """
        Get date with more sells
        :return:
        """
        try:
            transaction_dates_list = self.filter(company=company, final_payment=True, deleted=False).values('transaction_date').annotate(total_count=Count('transaction_date')).order_by(
                'total_count')
            return max(t.total_count for t in transaction_dates_list).transaction_date
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
