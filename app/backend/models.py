from django.db import models
from django.utils import timezone

class BotUser(models.Model):
    chat_id = models.IntegerField(unique=True, verbose_name='Айди')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name='Никнейм')
    language = models.CharField(
        max_length=5,
        choices=(
            ('eng', 'eng'),
            ('ru', 'ru')
        ),
        default='ru',
        verbose_name='Язык'
        )
    created = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    
    def __str__(self):
        return f'{self.full_name}'

    class Meta:
         verbose_name = "Пользователь"
         verbose_name_plural = 'Пользователи'

class Template(models.Model):
    title = models.CharField(max_length=255, verbose_name='Названия текста')
    body_ru = models.TextField(verbose_name='Русский текст')
    body_eng = models.TextField(verbose_name='Английский текст')

    class Meta:
         verbose_name = "Шаблон"
         verbose_name_plural = 'Шаблоны'


    def __str__(self) -> str:
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    users_count = models.IntegerField(null=True, blank=True)
    chat_id = models.IntegerField()
    black_list = models.TextField(null=True, blank=True)
    white_list = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name