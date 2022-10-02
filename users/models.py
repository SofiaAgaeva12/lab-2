from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import CreateView
import datetime


class Category(models.Model):
    """
    Model representing a category of record (e.g. ).
    """
    name = models.CharField(max_length=200, help_text="Enter a category of record", unique=True)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    class Meta:
        permissions = (("can_mark_returned", "Set record as returned"),)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)


class Record(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the record")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)

    category = models.ForeignKey(Category, to_field='name', help_text='Категория заявки', blank=False,
                                 on_delete=models.CASCADE)

    image = models.ImageField(upload_to='media/images/%Y-%m-%d/',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Опубликовано')

    comment = models.TextField(blank=True, help_text="Комментарий к записи")
    design = models.ImageField(blank=True, upload_to='media/images/%Y-%m-%d/')
    LOAN_STATUS = (
        ('n', 'Новая'),
        ('p', 'Выполнено'),
        ('a', 'Принято в работу'),
    )

    status = models.CharField(
        max_length=100,
        choices=LOAN_STATUS,
        blank=True,
        default='n',
        help_text='Record availability')

    # def delete(self, *args, **kwargs):
    #     for ai in self.additionalimage.all():
    #         ai.delete()
    #     super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявка'
        ordering = ['-created_at']
        permissions = (("can_mark_returned", "Set record as returned"),)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular record.
        """
        return reverse('record-detail', args=[str(self.id)])


from .utilities import get_timestamp_path


# class AdditionalImage(models.Model):
#     bb = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name='Заявки')
#     image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Заявка')
#
#     class Meta:
#         verbose_name_plural = 'Дополнительные иллюстрации'
#         verbose_name = 'Дополнительная иллюстрация'
