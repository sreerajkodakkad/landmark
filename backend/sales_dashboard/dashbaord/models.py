# dashbaord/models.py

from django.db import models

class Sales(models.Model):
    invoice_item_number = models.CharField(max_length=255, primary_key=True)  # Using invoice_item_number as the primary key
    Date = models.CharField(max_length=255)
    store_number = models.IntegerField()
    store_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    store_location = models.CharField(max_length=255)
    county_number = models.IntegerField()
    county = models.CharField(max_length=255)
    category = models.IntegerField()
    category_name = models.CharField(max_length=255)
    vendor_number = models.IntegerField()
    vendor_name = models.CharField(max_length=255)
    item_number = models.IntegerField()
    item_desc = models.CharField(max_length=255)
    pack = models.IntegerField()
    bottle_volume_ml = models.CharField(max_length=255)
    state_bottle_cost = models.FloatField()
    state_bottle_retail = models.FloatField()
    bottles_sold = models.IntegerField()
    sale_dollars = models.FloatField()
    volume_sold_liters = models.FloatField()
    volume_sold_gallons = models.FloatField()

    class Meta:
        db_table = 'csvdb'
