from django.db import models

# Create your models here.


class Bill(models.Model):
    bill_no = models.CharField(
        primary_key=True, null=False, blank=False, max_length=10)
    bill_date = models.DateField()
    from_field = models.CharField(blank=False, max_length=150)
    to_field = models.CharField(blank=False, max_length=150)
    customer_name = models.CharField(blank=False, max_length=150)
    customer_address_line_1 = models.TextField(blank=False, max_length=150)
    customer_address_line_2 = models.TextField(blank=True, max_length=150)
    customer_address_line_3 = models.TextField(blank=True, max_length=150)
    lr_no = models.CharField(max_length=150)
    lr_date = models.DateField(blank=True)
    invoice_no = models.CharField(max_length=150)
    truck_no = models.CharField(max_length=150)
    container_no = models.CharField(max_length=150)
    be_no = models.CharField(max_length=150)
    freight_charges = models.IntegerField(default=0)
    hamali_charges = models.IntegerField(default=0)
    halting_charges = models.IntegerField(default=0)
    weight_charges = models.IntegerField(default=0)
    bill_exchange_charges = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
