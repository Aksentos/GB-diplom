from django.contrib import admin
from .models import NewProcedures, Archive
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# класс обработки данных
class ProceduresResource(resources.ModelResource):

    class Meta:
        model = NewProcedures
        skip_unchanged = True
        report_skipped = True


# вывод данных на странице
class ProceduresAdmin(ImportExportModelAdmin):
    resource_classes = [ProceduresResource]


admin.site.register(NewProcedures, ProceduresAdmin)
admin.site.register(Archive)
