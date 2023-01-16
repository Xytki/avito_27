from django.db import models

# "name": "Сибирская котята, 3 месяца",
# "author": "Павел",
# "price": 2500,
# "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
# "address": "Москва, м. Студенческая",
# "is_published": true

class Ad(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    address = models.CharField(max_length=300)
    is_published = models.BooleanField()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
