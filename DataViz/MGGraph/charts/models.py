from django.db import models

# Create your models here.
class Experiment(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    fecha = models.DateField()
    comentarios = models.CharField(max_length=350, null=True)

    def __str__(self):
        return self.nombre
    
    
class CsvFile(models.Model):
    id_experimento = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    tiempo = models.IntegerField(null=True)

    def __str__(self):
        return self.id_experimento.nombre + ' - ' + self.nombre
    

class CsvFile_Col(models.Model):
    id_csvFile = models.ForeignKey(CsvFile, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
    numCol = models.IntegerField(null=True)

    def __str__(self):
        return self.id_csvFile.nombre + ' - ' + self.nombre
    
class Record(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_csvFile_Col = models.ForeignKey(CsvFile_Col, on_delete=models.CASCADE)
    tiempo = models.IntegerField()
    valor = models.FloatField()

    def __str__(self):
        return 'Time: ' + str(self.tiempo) + ' ' + self.id_csvFile_Col.nombre + ': ' + str(self.valor)

class Coordenate(models.Model):
    id_csvFile = models.ForeignKey(CsvFile, on_delete=models.CASCADE)
    puntoX = models.FloatField()
    puntoY = models.FloatField()
    
    def __str__(self):
        return self.id_csvFile.nombre + ' - ' + str(self.puntoX) + ',' + str(self.puntoY)