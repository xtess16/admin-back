from django.db import models


class AbstractBaseSave(models.Model):
    created_at = models.DateTimeField("Создан", auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField("Удален", null=True, blank=True)

    class Meta:
        abstract = True
