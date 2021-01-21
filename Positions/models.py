from django.db import models

# Create your models here.

class Groups (models.Model):
    id = models.AutoField(primary_key=True)  # ИД номенклатурной группы
    name = models.TextField # Имя группы


class Xyz (models.Model):
    id = models.AutoField(primary_key=True)  # ИД места хранения
    X = models.TextField  # Координаты ряда хранения
    y = models.IntegerField  # Координаты зоны ряда
    z = models.IntegerField  # Координаты уровня высоты


class Positions (models.Model):
    id = models.AutoField(primary_key=True) # ИД комлектующего
    code = models.PositiveBigIntegerField # Штрихкод
    name = models.TextField # Наименование
    groups_id = models.ForeignKey(Groups.id) # Номенклатурная группа
    quantity = models.FloatField # Количество
    ediz = models.CharField # Единица измерения
    photo1 = models.ImageField # Фото 1
    photo2 = models.ImageField # Фото 2 (в упаковке)
    mol = models.TextField # Материально-ответственное лицо
    xyz_id = models.ForeignKey(Xyz.id) # Местонахождение


class Levels(models.Model):
    id = models.AutoField(primary_key=True)  # ИД уровня доступа
    name = models.TextField  # Описание уровня доступа


class Persons (models.Model):
    id = models.AutoField(primary_key=True)  # ИД авторизованного пользователя
    name = models.TextField # Фамилия И.О.
    level_id = models.ForeignKey(Levels.id) # Уровень доступа


class Change_types(models.Model):
    id = models.AutoField(primary_key=True)  # ИД типа операции
    name = models.TextField  # Тип атомарной операции с комлпектующим
    znak = models.BooleanField # характеритика операции: True - увеличение, False - уменьшение количества


class Objects (models.Model):
    id = models.AutoField(primary_key=True)  # ИД объекта
    name = models.TextField  # Наименование объекта
    adress = models.TextField  # Адрес объекта


class Сhange_qality (models.Model):
    id = models.AutoField(primary_key=True) # ИД операции по изменению величины остатков
    time_oper = models.DateTimeField # Время совершения операции
    change_type_id = models.ForeignKey(Change_types.id, on_delete='') # Тип операции
    position_id = models.ForeignKey(Positions.id) # ИД  комплектующего
    quantity = models.FloatField # Количество
    person_id_mol = models.ForeignKey(Persons.id) # ИД МОЛ
    person_id_contr = models.ForeignKey(Persons.id)  # ИД подотчетного лица
    object_id = models.ForeignKey(Objects.id)  # ИД объекта