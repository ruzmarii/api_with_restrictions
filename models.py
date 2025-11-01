from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления"""
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"

class Advertisement(models.Model):
    """Объявление"""
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание", blank=True, default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def clean(self):
        """Валидация: не больше 10 открытых объявлений у пользователя"""
        if self.status == AdvertisementStatusChoices.OPEN and self.creator:
            open_ads_count = Advertisement.objects.filter(
                creator=self.creator,
                status=AdvertisementStatusChoices.OPEN
            ).exclude(pk=self.pk).count()
            
            if open_ads_count >= 10:
                raise ValidationError("У пользователя не может быть больше 10 открытых объявлений")

    def save(self, *args, **kwargs):
        """Переопределяем save для вызова валидации"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'advertisements'
        ordering = ['-created_at']