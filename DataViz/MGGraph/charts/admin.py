from django.contrib import admin
from .models import Experiment, CsvFile, CsvFile_Col, Record, Coordenate

# Register your models here.
admin.site.register(Experiment)
admin.site.register(CsvFile)
admin.site.register(CsvFile_Col)
admin.site.register(Record)
admin.site.register(Coordenate)