from django.db import models


class AP(models.Model):
    name = models.CharField(max_length=45, null=False)
    email = models.CharField(max_length=45, null=False)
    password = models.CharField(primary_key=True, max_length=45, null=False)
    number = models.IntegerField(null=False)

    class Meta:
        db_table = 'uber'
