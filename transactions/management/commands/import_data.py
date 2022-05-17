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
        try:
            start_date = datetime.strptime('1/1/2019 1:30 PM', '%m/%d/%Y %I:%M %p')
            end_date = datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p')

            file_path = settings.DB_DATA_PATH
            with open(file_path) as f:
                content = f.readlines()
            header = content[:1]
            rows = content[1:]
            print(header)
            print(rows)

            for row in rows:
                try:
                    company = row[0]
                    price = row[1]
                    date = row[2]
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
                        # generate ramdom date
                        generated_date = random_date(start_date, end_date)
                        # fix status for database
                        boolean_transaction_status = True if status_transaction.strip() == 'true' else False
                        # fix approved for database
                        boolean_approved_status = True if status_approved.strip() == 'true' else False

                        Transaction.objects.get(company=db_company, price=Decimal(str(str_price)),
                                                transaction_date=generated_date, status=boolean_transaction_status,
                                                approved=boolean_approved_status)
                    except Transaction.DoesNotExist:
                        t = Transaction(company=db_company, price=Decimal(str(str_price)),
                                        transaction_date=generated_date,
                                        status=boolean_transaction_status, approved=boolean_approved_status)
                        t.save()  # for ensure the execution of the function for complete final_payment

                except Exception as ex:
                    print str(ex)
                    pass

        except Exception as ex:
            print str(ex)
            raise

