# -*- encoding: utf-8 -*-
import traceback
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from transactions.models import Company, Transaction
from transactions.utils import random_date


class Command(BaseCommand):
    help = 'Import data to the database'

    def handle(self, *args, **options):
        try:
            self.import_data()
        except Exception as ex:
            raise CommandError(traceback.format_exc())

    def import_data(self):
        """
        Import data from file to the database
        :return:
        """
        from decimal import Decimal
        from csv import reader
        try:
            file_path = settings.DB_DATA_PATH
            with open(file_path) as f:
                # pass the file object to reader() to get the reader object
                csv_reader = reader(f)
                # Iterate over each row in the csv using reader object
                for row in csv_reader:
                    # row variable is a list that represents a row in csv
                    try:
                        company = row[0]
                        price = row[1]
                        str_date = row[2]
                        status_transaction = row[3]
                        status_approved = row[4]

                        try:
                            db_company = Company.objects.get(name=company.strip())
                        except Company.DoesNotExist:
                            if not company.strip():
                                company = 'Unnamed'
                            db_company = Company.objects.create(name=company.strip())

                        try:
                            # fix the price
                            str_price = price.strip()
                            # get date from file
                            trans_date = datetime.strptime(str_date[:19], '%Y-%m-%d %H:%M:%S')
                            # fix status for database
                            transaction_status = status_transaction.strip()
                            # fix approved for database
                            boolean_approved_status = True if status_approved.strip() == 'true' else False

                            Transaction.objects.get(company=db_company, price=Decimal(str(str_price)),
                                                    transaction_date=trans_date, status=transaction_status,
                                                    approved=boolean_approved_status)
                        except Transaction.DoesNotExist:
                            t = Transaction(company=db_company, price=Decimal(str(str_price)),
                                            transaction_date=trans_date,
                                            status=transaction_status, approved=boolean_approved_status)
                            t.save()  # for ensure the execution of the function for complete final_payment

                    except Exception as ex:
                        print str(ex)
                        pass

        except Exception as ex:
            print str(ex)
            raise

