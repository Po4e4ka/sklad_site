from django.db import models

# Create your models here.

class Groups (models.Model):
    id = models.AutoField(primary_key=True)  # ИД номенклатурной группы
    name = models.TextField(null=True) # Имя группы


class Xyz (models.Model):
    id = models.AutoField(primary_key=True)  # ИД места хранения
    X = models.TextField(null=True)  # Координаты ряда хранения
    y = models.IntegerField(null=True)  # Координаты зоны ряда
    z = models.IntegerField(null=True)  # Координаты уровня высоты


class Levels(models.Model):
    id = models.AutoField(primary_key=True)  # ИД уровня доступа
    name = models.TextField(null=True)  # Описание уровня доступа


class Persons (models.Model):
    id = models.AutoField(primary_key=True)  # ИД авторизованного пользователя
    name = models.TextField(null=True) # Фамилия И.О.
    level_id = models.ForeignKey(Levels,on_delete=models.SET_NULL, null=True) # Уровень доступа


class Positions (models.Model):
    # функция ввода vvod_info_pos проверяет отсутствие дублирования по полю "name"
    id = models.AutoField(primary_key=True) # ИД комлектующего
    code = models.PositiveBigIntegerField(null=True) # Штрихкод
    name = models.TextField(null=True) # Наименование
    groups_id = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True) # Номенклатурная группа
    quantity = models.FloatField(null=True) # Количество
    ediz = models.TextField(null=True) # Единица измерения
    photo1 = models.ImageField(null=True, blank=True, upload_to="images/") # Фото 1
    photo2 = models.ImageField(null=True, blank=True, upload_to="images/") # Фото 2 (в упаковке)
    mol = models.ForeignKey(Persons, on_delete=models.SET_NULL, null=True) # Материально-ответственное лицо
    xyz_id = models.ForeignKey(Xyz, on_delete=models.SET_NULL, null=True) # Местонахождение


class Change_types(models.Model):
    id = models.AutoField(primary_key=True)  # ИД типа операции
    name = models.TextField(null=True)  # Тип атомарной операции с комлпектующим
    znak = models.BooleanField(null=True) # Характеритика операции: True - увеличение, False - уменьшение количества


class Objects (models.Model):
    id = models.AutoField(primary_key=True)  # ИД объекта
    name = models.TextField(null=True)  # Наименование объекта
    adress = models.TextField(null=True)  # Адрес объекта


class Change_qantity (models.Model):
    id = models.AutoField(primary_key=True) # ИД операции по изменению величины остатков
    time_oper = models.DateTimeField(null=True) # Время совершения операции
    change_type_id = models.ForeignKey(Change_types, on_delete=models.SET_NULL, null=True ) # Тип операции
    position_id = models.ForeignKey(Positions, on_delete=models.SET_NULL, null=True) # ИД  комплектующего
    quantity = models.FloatField(null=True) # Количество
    person_id_mol = models.ForeignKey(Persons, on_delete=models.SET_NULL, null=True, related_name="mol") # ИД МОЛ
    person_id_contr = models.ForeignKey(Persons, on_delete=models.SET_NULL, null=True, related_name='contr')  # ИД подотчетного лица
    object_id = models.ForeignKey(Objects, on_delete=models.SET_NULL, null=True)  # ИД объекта