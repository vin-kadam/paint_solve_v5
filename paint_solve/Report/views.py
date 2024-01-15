from django.shortcuts import reverse
from django.http import HttpResponse, HttpRequest
from Inventory.models import Product, Stock, Brand
from transaction.models import Sale, Purchase
from django.db.models import Sum
from datetime import datetime, timedelta
from io import BytesIO
from django.template.loader import render_to_string
from django.views import View
from django.utils import timezone
from reportlab.pdfgen import canvas
from django.db.models import Sum

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle,Spacer
from reportlab.lib import colors

import pygal
from Dashboard.views import get_dashboard_data
from django.contrib.auth.decorators import login_required
import os


class MonthlySalesReportView(View):
    template_name = 'Reports/monthly_sales_report_template.html'

    def get(self, request, *args, **kwargs):
        current_date = datetime.now()
        start_date = datetime(current_date.year, current_date.month, 1)
        end_date = start_date + timedelta(days=31)


        monthly_sales = Sale.objects.filter(sale_date__range=[start_date, end_date])
        monthly_purchases = Purchase.objects.filter(purchase_date__range=[start_date, end_date])

        products_data = []
        for product in Product.objects.all():
            sales_for_product = monthly_sales.filter(product=product)
            total_sales = sales_for_product.aggregate(total_sales=Sum('price'))['total_sales'] or 0
            total_quantity_sold = sales_for_product.aggregate(total_quantity_sold=Sum('quantity'))['total_quantity_sold'] or 0

            products_data.append({
                'product_name': product.color_name,
                'total_sales': total_sales,
                'total_quantity_sold': total_quantity_sold
            })

        purchases_data = []
        for product in Product.objects.all():
            purchases_for_product = monthly_purchases.filter(product=product)
            total_purchase = purchases_for_product.aggregate(total_purchase=Sum('price'))['total_purchase'] or 0

            purchases_data.append({
                'product_name': product.color_name,
                'category': product.category,
                'total_purchase': total_purchase
            })

        
        most_sold_by_category = Sale.objects.filter(sale_date__range=[start_date, end_date]).values(
            'product__category'
        ).annotate(total_quantity_sold=Sum('quantity')).order_by('-total_quantity_sold').first()

        most_purchased_by_category = Purchase.objects.filter(purchase_date__range=[start_date, end_date]).values(
            'product__category'
        ).annotate(total_purchase=Sum('price')).order_by('-total_purchase').first()

        most_sold_by_brand = Sale.objects.filter(sale_date__range=[start_date, end_date]).values(
            'product__brand__name'
        ).annotate(total_quantity_sold=Sum('quantity')).order_by('-total_quantity_sold').first()

        most_purchased_by_brand = Purchase.objects.filter(purchase_date__range=[start_date, end_date]).values(
            'product__brand__name'
        ).annotate(total_purchase=Sum('price')).order_by('-total_purchase').first()

        total_transactions = monthly_sales.count() + monthly_purchases.count()

       
        context = {
            'products_data': products_data,
            'purchases_data': purchases_data,
            'most_sold_by_category': most_sold_by_category,
            'most_purchased_by_category': most_purchased_by_category,
            'most_sold_by_brand': most_sold_by_brand,
            'most_purchased_by_brand': most_purchased_by_brand,
            'total_transactions': total_transactions,
            'now': datetime.now(),
            'start_date': start_date,
            'end_date': end_date,
            'total_purchases': sum(purchase['total_purchase'] for purchase in purchases_data)
        }

       
        html_content = render_to_string(self.template_name, context)

        
        pdf_data = self.generate_pdf(html_content,
        context,
        start_date,
        end_date,
        most_sold_by_category,
        most_purchased_by_category,
        most_sold_by_brand,
        most_purchased_by_brand,
        total_transactions)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="monthly_sales_report.pdf"'
        response.write(pdf_data)
        return response

    def generate_pdf(self, html_content, context, start_date, end_date, most_sold_by_category, 
                 most_purchased_by_category, most_sold_by_brand, most_purchased_by_brand,
                 total_transactions):
        buffer = BytesIO()
        
        # Setting up style for bold text
        style = getSampleStyleSheet()
        bold_style = style["Heading1"]
        bold_style.textColor = colors.black

        
        elements = []

        
        elements.append(Spacer(1, 24))  
        elements.append(Paragraph("<b>MAHAVIR PAINT SHOP</b>", bold_style))
        elements.append(Spacer(1, 36)) 
        
        
        table_header_sales = ["Product", "Total Sales", "Total Quantity Sold"]
        sales_table_data = [
            table_header_sales,
            *[list(data.values()) for data in context['products_data']]
        ]

        sales_table = Table(sales_table_data)
        sales_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                         ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(sales_table)
        elements.append(Spacer(1, 36))  

        
        table_header_purchases = ["Product", "Category", "Total Purchase"]
        purchases_table_data = [
            table_header_purchases,
            *[list(data.values()) for data in context['purchases_data']]
        ]

        purchases_table = Table(purchases_table_data)
        purchases_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                             ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                             ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(purchases_table)

        
        elements.append(Spacer(1, 36))  
        elements.append(Paragraph(f"<b>Additional Information:</b>", bold_style))
        elements.append(Paragraph(f"Most Sold by Category: {most_sold_by_category}", style['Normal']))
        elements.append(Paragraph(f"Most Purchased by Category: {most_purchased_by_category}", style['Normal']))
        elements.append(Paragraph(f"Most Sold by Brand: {most_sold_by_brand}", style['Normal']))
        elements.append(Paragraph(f"Most Purchased by Brand: {most_purchased_by_brand}", style['Normal']))
        elements.append(Paragraph(f"Total Transactions: {total_transactions}", style['Normal']))
        

      
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        doc.build(elements)

        buffer.seek(0)
        return buffer.getvalue()

    def draw_table(self, pdf, data, x, y, col_widths):
        row_height = 20
        for row in data:
            for i, value in enumerate(row):
                pdf.rect(x, y, col_widths[i], row_height)
                pdf.drawString(x + 3, y + 3, str(value))
                x += col_widths[i]
            x = 100
            y -= row_height

    def draw_text(self, pdf, text, x, y):
        pdf.drawString(x, y, text)



   
   


# # Create your views here.
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from io import BytesIO
# from inventory.models import Stock,Product,Supplier,Brand
# from Transaction.models import Sale
# from django.db.models import Sum
# from datetime import datetime, timedelta

# def generate_monthly_sales_report(request):
#     current_date = datetime.now()
#     current_month = current_date.month
#     current_year = current_date.year

#    
#     start_date = datetime(current_year, current_month, 1)
#     end_date = start_date + timedelta(days=31)  # Considering a maximum of 31 days in a month

#     
#     monthly_sales = Sale.objects.filter(sale_date__range=[start_date, end_date])

#    
#     products_data = []
#     for product in Product.objects.all():
#         sales_for_product = monthly_sales.filter(product=product)
#         total_sales = sales_for_product.aggregate(total_sales=Sum('price'))['total_sales'] or 0
#         total_quantity_sold = sales_for_product.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

#         products_data.append({
#             'product': product,
#             'total_sales': total_sales,
#             'total_quantity_sold': total_quantity_sold
#         })

#    
#     buffer = BytesIO()
#     pdf = canvas.Canvas(buffer)

#     
#     pdf.drawString(100, 800, 'Monthly Sales Report')
#     y_coordinate = 780
#     for data in products_data:
#         product_name = data['product'].color_name
#         total_sales = data['total_sales']
#         total_quantity_sold = data['total_quantity_sold']
        
#         pdf.drawString(100, y_coordinate, f"Product: {product_name}")
#         pdf.drawString(120, y_coordinate - 20, f"Total Sales: ${total_sales}")
#         pdf.drawString(120, y_coordinate - 40, f"Total Quantity Sold: {total_quantity_sold}")
#         y_coordinate -= 60

#     pdf.save()
#     buffer.seek(0)

#     
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="monthly_sales_report.pdf"'
#     response.write(buffer.getvalue())
#     return response
