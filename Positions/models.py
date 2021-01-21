from django.db import models

# Create your models here.

class Groups (models.Model):
    id = models.AutoField(primary_key=True)  # ИД номенклатурной группы
    name = models.TextField() # Имя группы


class Xyz (models.Model):
    id = models.AutoField(primary_key=True)  # ИД места хранения
    X = models.TextField()  # Координаты ряда хранения
    y = models.IntegerField()  # Координаты зоны ряда
    z = models.IntegerField()  # Координаты уровня высоты


class Positions (models.Model):
    id = models.AutoField(primary_key=True) # ИД комлектующего
    code = models.PositiveBigIntegerField() # Штрихкод
    name = models.TextField() # Наименование
    groups_id = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True) # Номенклатурная группа
    quantity = models.FloatField() # Количество
    ediz = models.TextField() # Единица измерения
    photo1 = models.ImageField() # Фото 1
    photo2 = models.ImageField() # Фото 2 (в упаковке)
    mol = models.TextField() # Материально-ответственное лицо
    xyz_id = models.ForeignKey(Xyz, on_delete=models.SET_NULL, null=True) # Местонахождение


class Levels(models.Model):
    id = models.AutoField(primary_key=True)  # ИД уровня доступа
    name = models.TextField()  # Описание уровня доступа


class Persons (models.Model):
    id = models.AutoField(primary_key=True)  # ИД авторизованного пользователя
    name = models.TextField() # Фамилия И.О.
    level_id = models.ForeignKey(Levels,on_delete=models.SET_NULL, null=True) # Уровень доступа


class Change_types(models.Model):
    id = models.AutoField(primary_key=True)  # ИД типа операции
    name = models.TextField()  # Тип атомарной операции с комлпектующим
    znak = models.BooleanField() # характеритика операции: True - увеличение, False - уменьшение количества


class Objects (models.Model):
    id = models.AutoField(primary_key=True)  # ИД объекта
    name = models.TextField()  # Наименование объекта
    adress = models.TextField()  # Адрес объекта


class Change_qantity (models.Model):
    id = models.AutoField(primary_key=True) # ИД операции по изменению величины остатков
    time_oper = models.DateTimeField() # Время совершения операции
    change_type_id = models.ForeignKey(Change_types, on_delete=models.SET_NULL, null=True ) # Тип операции
    position_id = models.ForeignKey(Positions, on_delete=models.SET_NULL, null=True) # ИД  комплектующего
    quantity = models.FloatField() # Количество
    person_id_mol = models.ForeignKey(Persons, on_delete=models.SET_NULL, null=True, related_name="mol") # ИД МОЛ
    person_id_contr = models.ForeignKey(Persons, on_delete=models.SET_NULL, null=True, related_name='contr')  # ИД подотчетного лица
    object_id = models.ForeignKey(Objects, on_delete=models.SET_NULL, null=True)  # ИД объекта