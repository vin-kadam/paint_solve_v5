from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Purchase, Sale, Stock,Product
from django.contrib import messages
                
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'supplier', 'quantity', 'price']
    

    
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return quantity

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row g-3'
        self.helper.layout = Layout(
             Row(
                Column('product', css_class='form-group col-md-6'),
                Column('supplier', css_class='form-group col-md-6'),
                css_class='mb-3'
            ),
            'quantity',
            'price',
            Submit('submit', 'Submit', css_class='btn btn-light')
        )
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.color_name} - {obj.brand} - {obj.category} - {obj.color_code} "

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'customer_name', 'customer_phone_no', 'customer_email', 'quantity', 'price']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.cleaned_data['product']

        try:
            stock = Stock.objects.get(product=product)
            available_quantity = stock.quantity
        except Stock.DoesNotExist:
            available_quantity = 0

        if quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        elif quantity > available_quantity:
            message = f"{product.color_name} is at low stock."
            messages.error(self.request, message)  # Add an error message
            raise forms.ValidationError(message)

        return quantity

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})  # Update the widget attribute for the product field
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row g-3'
        self.helper.layout = Layout(
            'product',  # Include the product field
            'customer_name',
            'customer_phone_no',
            'customer_email',
            'quantity',
            'price',
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.color_name} - {obj.brand} - {obj.category} - {obj.color_code} "
    
       

# from inventory.models import Stock

# class SalesForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['product', 'quantity']

#     def clean_quantity(self):
#         quantity = self.cleaned_data['quantity']
#         product = self.cleaned_data['product']

#         if product.quantity < quantity:
#             raise forms.ValidationError('Not enough stock available.')

#         return quantity

# class PurchaseForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['product', 'quantity', 'price']

#     def clean_quantity(self):
#         quantity = self.cleaned_data['quantity']
#         if quantity < 0:
#             raise forms.ValidationError('Quantity cannot be negative.')

#         return quantity