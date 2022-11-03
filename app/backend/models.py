from django.db import models
from django.utils import timezone

class BotUser(models.Model):
    chat_id = models.IntegerField(unique=True, verbose_name='Айди')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name='Никнейм')
    group_id_state = models.CharField(max_length=255,default=0)
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

class Template2Button(models.Model):
    title = models.CharField(max_length=255, verbose_name='Названия текста')
    body_ru = models.TextField(verbose_name='Русский текст')
    body_eng = models.TextField(verbose_name='Английский текст')

    class Meta:
         verbose_name = "Шаблон для кнопки"
         verbose_name_plural = 'Шаблоны для кнопок'


    def __str__(self) -> str:
        return self.title

class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name='Названия')
    username = models.CharField(max_length=255, default='-', verbose_name='Никнейм', blank=True)
    link = models.CharField(max_length=255, default='-', verbose_name='Ссылка', blank=True)
    description = models.TextField(default='-', verbose_name='Описания')
    users_count = models.IntegerField(default=0, verbose_name='Кол-во пользователей')
    chat_id = models.IntegerField(default=10, verbose_name='Чат айди')
    black_list = models.TextField(default='-', verbose_name='Черный список')
    enable_black_list = models.BooleanField(default=False, verbose_name='Вкл/Выкл черный список')
    black_list_timer = models.IntegerField(default=10, verbose_name='Таймер черного списка')
    white_list = models.TextField(default='-', verbose_name='Белый список')
    enable_white_list = models.BooleanField(default=False, verbose_name='Вкл/Выкл белый список')
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    type = models.CharField(
        max_length=255, 
        choices=(
            ('Chanel', 'Канал'),
            ('Chat', 'Чат')
        ),
        default='Chanel', 
        verbose_name='Тип'
        )
    filter_photo = models.BooleanField(default=True, verbose_name='Фото')
    filter_text = models.BooleanField(default=True, verbose_name='Текст')
    filter_voice = models.BooleanField(default=True, verbose_name='Голосовое')
    filter_video_note = models.BooleanField(default=True, verbose_name='Кружок')
    filter_video = models.BooleanField(default=True, verbose_name='Видео')
    filter_document = models.BooleanField(default=True, verbose_name='Документ')

    class Meta:
         verbose_name = "Чат"
         verbose_name_plural = 'Чаты'
         
    def __str__(self) -> str:
        return self.title