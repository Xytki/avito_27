from django.db import models

# "name": "Сибирская котята, 3 месяца",
# "author": "Павел",
# "price": 2500,
# "description": "Продаю сибирских котят, возвраст 3 месяца.\nОчень милые и ручные.\nЛоточек знают на пятерку, кушают премиум корм.\nЖдут любящих и заботливых хояев. Больше фотографий отправлю в личку, цена указана за 1 котенка.",
# "address": "Москва, м. Студенческая",
# "is_published": true

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Ad(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    is_published = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ad_picture", null=True, blank=True)

    class Meta:
        verbose_name = "Объявления"
        verbose_name_plural = "Объявлении"

    def __str__(self):
        return self.name



