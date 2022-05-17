# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _
from .managers import CompanyManager, TransactionManager
# Create your models here.


class Company(models.Model):
    """
    Models for track companies
    """
    STATUSES = Choices(
        ('active', _('active')),
        ('inactive', _('inactive')))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # company name
    name = models.CharField(max_length=50)
    # company status
    status = models.IntegerField(choices=STATUSES, default=STATUSES.active)
    # logically delete for keep the track on deleted companies
    deleted = models.BooleanField(default=False)

    objects = CompanyManager()

    def __unicode__(self):
        # transaction reference and representation
        return str(self.name).upper()


class Transaction(models.Model):
    """
    Model for track the transactions
    """
    STATUSES = Choices(
        ('pending', _('pending')),
        ('reversed', _('reversed')),
        ('closed', _('closed')))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # transaction related company
    company = models.ForeignKey(Company, related_name="transactions")
    # transaction price
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # store the date when registry was created
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    # store the date of the transaction
    transaction_date = models.DateTimeField()
    # transaction status
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUSES.pending)
    # status approval
    approved = models.BooleanField(default=False)
    # logically delete for keep the track of deleted transactions
    deleted = models.BooleanField(default=False)
    # check if this price it's the final payment
    final_payment = models.BooleanField(default=False)

    objects = TransactionManager()

    def __unicode__(self):
        # transaction reference and representation
        return '{} - {}'.format(str(self.company.name).upper(), self.id)

    def save(self, *args, **kwargs):
        # This can be improved using django signals
        self.final_payment = True if self.status == 'closed' and self.approved else False
        super(Transaction, self).save(*args, **kwargs)


# class SystemUser(AbstractUser):
#     second_email = models.EmailField(null=True, blank=True)
#     phone = models.CharField(max_length=50, null=True, blank=True)
#     deleted = models.BooleanField(default=False)
#
#     objects = SystemUserManager()
#
#     def __unicode__(self):
#         return self.username
#
#     class Meta:
#         managed = True
#         db_table = 'systemuser'
