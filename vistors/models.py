from django.db import models
from django.contrib.auth.models import User
from messages import messages
# Create your models here.


class Vistor(models.Model):
    """
        vistor/tenant model representation
    """
    name = models.CharField(max_length=250, blank=False, null=False)
    tel_number = models.CharField(max_length=15, blank=False, null=False,
                                  unique=True)
    company = models.CharField(max_length=250, blank=True, null=True)
    created_by = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    tenant = models.BooleanField(default=False)

    def validate(self):
        print("validating")
        valid = True
        errors = {}
        if not self.name:
            errors['name'] = messages.FIELD_REQUIRED.format("name", "vistor")
            valid = False

        if not self.tel_number:
            errors['tel_number'] = messages.FIELD_REQUIRED.format(
                "tel_number", "vistor")
            valid = False

        if int(self.tenant) == 1 and not self.company:
            errors['company'] = messages.FIELD_REQUIRED.format(
                "company", "tenants")
            valid = False

        return valid, errors


class Entry(models.Model):
    """
        vistor/ tenant daily entry/log
    """
    vistor = models.ForeignKey(Vistor, null=False, on_delete=models.CASCADE)
    temperature = models.FloatField(null=False, blank=False)
    time_stamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    destination = models.CharField(max_length=50, null=True)

    def validate(self):
        valid = True
        errors = {}
        print('validate entry')
        print(self.destination)
        print(self.vistor.tenant)
        if not self.temperature:
            errors['temperature'] = messages.FIELD_REQUIRED.format(
                "temperature", "entry")
            valid = False

        if (int(self.vistor.tenant) == 0) and (not self.destination):
            errors['destination'] = messages.FIELD_REQUIRED.format(
                "destination", "vistors")
            valid = False
        return valid, errors
