from django.urls import path
from .views import index, export_csv, get_all_bills, get_result, get_statement, get_statistics, get_vehicle_report, generate_bill, home, edit_bill, delete_bill


app_name = 'frontend'

urlpatterns = [
    path('', home),
    path('form/', index),
    path('generate/', generate_bill),
    path('statement/', get_statement),
    path('vehicle-report/', get_vehicle_report),
    path('dashboard/', get_statistics),
    path('all-bills/', get_all_bills),
    path('export-csv/<str:req_type>/', export_csv, name="export_url"),
    path('result/<str:bill_id>', get_result),
    path('edit/<str:bill_id>', edit_bill),
    path('delete/<str:bill_id>', delete_bill),
]
