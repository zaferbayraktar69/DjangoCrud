from django.db import models

# Veritabanımızdaki tabloların modellerini oluşturduk

class CategoryModel(models.Model):

    kategori=models.CharField(max_length=150)

    class Meta:
        db_table ="kategori"

    def __str__(self):
        return self.kategori



class IhaModel(models.Model):
    marka=models.CharField(max_length=150)
    model=models.CharField(max_length=150)
    agirlik=models.CharField(max_length=150)
  #  kategori=models.CharField(max_length=150)
    kategori = models.ForeignKey(CategoryModel, null=True ,  on_delete=models.SET_NULL)

    class Meta:
        db_table ="iha"



class UserModel(models.Model):

    adi=models.CharField(max_length=150)
    soyadi=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    sifre=models.CharField(max_length=150)
    
    class Meta:
        db_table ="kullanicilar"





