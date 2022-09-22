from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """
    Model representing a category of record (e.g. ).
    """
    name = models.CharField(max_length=200, help_text="Enter a category of record")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)


class Record(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the record")
    category = models.ManyToManyField(Category, help_text="Select a genre for this book")
    image = models.ImageField(upload_to='media/images/%Y-%m-%d/')
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