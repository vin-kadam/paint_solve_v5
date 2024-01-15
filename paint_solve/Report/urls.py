from django.urls import path
from Report.views import MonthlySalesReportView

urlpatterns = [
    path('monthly_sales_report_view/', MonthlySalesReportView.as_view(), name='monthly_sales_report_view'),
]