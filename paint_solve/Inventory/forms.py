from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.bootstrap import FormActions
from .models import Stock,Brand,Product,Supplier # Import your Stock model
CATEGORY = (
    ('Oil Paint','Oil Paint'),
    ('Cement Paint','Cement Paint'),
    ('Distemper Paint','Distemper Paint'),
    ('Emulsion Paint','Emulsion Paint'),
    ('Whitewash','Whitewash'),
    ('Enamel Paint','Enamel Paint'),
    ('Acrylic Emulsion Paint','Acrylic Emulsion Paint'),
    ('Bituminous Paint','Bituminous Paint'),
    ('Synthetic Rubber Paint','Synthetic Rubber Paint'),
    ('Anti-Corrosion Paint','Anti-Corrosion Paint'),
    
)

BRAND = (
    ('Asian Paints','Asian Paints'),
    ('Berger Paints','Berger Paints'),
    ('Kansai Nerolac Paints','Kansai Nerolac Paints'),
    ('AkzoNobel India','AkzoNobel India'),
    ('Indigo Paints','Indigo Paints'),
    ('Nippon Paints','Nippon Paints'),
    ('Shalimar Paints','Shalimar Paints'),	
    ('Dulux Paints','Dulux Paints'),
    ('Jenson & Nicholson Paints','Jenson & Nicholson Paints'),	
    ('Sheenlac Paints','Sheenlac Paints'),
    )
# class AddRecordForm(forms.ModelForm):
    
#     class Meta:
#         model = Stock
#         fields = '__all__'





# # Color_name = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={"placeholder":"Color Name","class":"form-control"}),label="")
#     # Category = forms.CharField(required=True,choices=CATEGORY,widget=forms.widgets.ChoiceWidget(attrs={"placeholder":"Category ","class":"form-control"}),label="")
#     # Brand = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={"placeholder":"Brand ","class":"form-control"}),label="")
#     # Color_code = forms.CharField(required=True,widget=forms.widgets.NumberInput(attrs={"placeholder":"Color Code","class":"form-control"}),label="")
#     # quantity = forms.CharField(required=True,widget=forms.widgets.NumberInput(attrs={"placeholder":"Quantity","class":"form-control"}),label="")
#     # price = forms.CharField(required=True,widget=forms.widgets.NumberInput(attrs={"placeholder":"Price","class":"form-control"}),label="")

#==============================================================================product========================================================================== 
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['color_name', 'category', 'brand', 'color_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['brand'].widget.attrs.update({'class': 'form-control'})
        self.fields['color_code'].widget.attrs.update({'class': 'form-control'})

        self.helper = FormHelper()
        self.helper.form_class = 'row g-3'
        self.helper.layout = Layout(
            'color_name',
            'category',
            'brand',
            'color_code',
            Submit('submit', 'Add Product', css_class='btn btn-primary')
            
        )
class ProductSearchForm(forms.Form):
    CATEGORY_CHOICES = (
        ('', 'Select Category'), 
        ('Oil Paint', 'Oil Paint'),
        ('Cement Paint', 'Cement Paint'),
    ('Distemper Paint', 'Distemper Paint'),
    ('Emulsion Paint', 'Emulsion Paint'),
    ('Whitewash', 'Whitewash'),
    ('Enamel Paint', 'Enamel Paint'),
    ('Acrylic Emulsion Paint', 'Acrylic Emulsion Paint'),
    ('Bituminous Paint', 'Bituminous Paint'),
    ('Synthetic Rubber Paint', 'Synthetic Rubber Paint'),
    ('Anti-Corrosion Paint', 'Anti-Corrosion Paint'),
    
        
    )

    # Fetching brand choices from the Brand model
    BRAND_CHOICES = [('', 'Select Brand')] + [(brand.name, brand.name) for brand in Brand.objects.all()]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select border-3 shadow-sm'})
    )
    brand = forms.ChoiceField(
        choices=BRAND_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select border-3 shadow-sm'})
    )
    color_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control border-3 shadow-sm'})
    )
#==============================================================================Stock========================================================================== 

class AddStockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['product', 'quantity', 'price', 'alert_threshold']

    def __init__(self, *args, **kwargs):
        super(AddStockForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.helper = FormHelper()
        self.helper.form_class = 'row g-3'
        self.helper.layout = Layout(
            'product',
            'quantity',
            'price',
            'alert_threshold',
            Submit('submit', 'Add Stock', css_class='btn btn-primary')
        )
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.color_name} - {obj.brand} - {obj.category} - {obj.color_code} "

class StockSearchForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'Select Category')] + list(Product.CATEGORY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control border-3 shadow-sm'}),
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        empty_label='Select Brand',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control border-3 shadow-sm'}),
    )

    color_code = forms.CharField(
        label='Color Code',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control border-3 shadow-sm'}),
    )
    
# class StockSearchForm(forms.ModelForm):
#     category = forms.ModelChoiceField(
#         queryset=Stock.objects.values_list('product__category', flat=True).distinct(),
#         widget=forms.Select(attrs={'class': 'form-select'}),
#         required=False,
#         label='Category'  # Set the label for the category field
#     )
#     brand = forms.ModelChoiceField(
#         queryset=Stock.objects.values_list('product__brand', flat=True).distinct(),
#         widget=forms.Select(attrs={'class': 'form-select'}),
#         required=False,
#         label='Brand'  # Set the label for the brand field
#     )

#     class Meta:
#         model = Stock
#         fields = ['category', 'brand']

#     def __init__(self, *args, **kwargs):
#         super(StockSearchForm,self).__init__(*args, **kwargs)
#         for field_name in self.fields:
#             self.fields[field_name].required = False
#         self.helper = FormHelper()
#         self.helper.form_class = 'row g-3'  # Bootstrap 5 form class
#         self.helper.layout = Layout(
#             Row(
#                 Column('category', css_class='col-md-6'),
#                 Column('brand', css_class='col-md-6'),
#                 css_class='mb-3'
#             ),
#             FormActions(
#                 Submit('submit', 'Search', css_class='btn btn-primary')
#             )
#         )

#         # Apply styles to labels directly in the form definition
#         self.fields['category'].label = 'Category'
#         self.fields['category'].widget.attrs.update({'class': 'form-label-custom'})
#         self.fields['brand'].label = 'Brand'
#         self.fields['brand'].widget.attrs.update({'class': 'form-label-custom'})

#==============================================================================Supplier========================================================================== 

class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'supplier_phone_no', 'supplier_email', 'supplied_products']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['supplied_products'].widget.attrs.update({'class': 'form-select', 'multiple': 'true'})

    class Media:
        js = ('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js',)
        css = {'all': ('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css',)}


class SupplierSearchForm(forms.Form):
    supplier_name = forms.CharField(
        label='Supplier Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control border-3 shadow-sm'}),
    )

    supplier_email = forms.EmailField(
        label='Supplier Email',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control border-3 shadow-sm'}),
    )

# class IssueStockForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = [ 'quantity']

#     def clean_quantity(self):
#         quantity = self.cleaned_data['quantity']
#         product = self.cleaned_data['product']

#         if product.quantity < quantity:
#             raise forms.ValidationError('Not enough quantity available.')

#         return quantity


# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = ['Supplier_Name', 'Supplier_Phone_number', 'product']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add fields from the Product model to the form
#         product_fields = ['Color_name', 'Category', 'Brand', 'Color_code', 'quantity', 'price']
#         for field in product_fields:
#             self.fields[field] = forms.CharField()  
            
            
            
# class SupplierAddForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = ['Supplier_Name', 'Supplier_Phone_number', 'color_name', 'Color_code', 'category', 'brand', 'quantity', 'price']

#     color_name = forms.CharField(max_length=100)
#     category = forms.ChoiceField(choices=CATEGORY)
#     brand = forms.ChoiceField(choices=BRAND)
#     Color_code = forms.CharField(max_length=100)
#     quantity = forms.IntegerField()
#     price = forms.IntegerField()

#     def clean(self):
#         cleaned_data = super().clean()
#         quantity = cleaned_data.get('quantity')
#         price = cleaned_data.get('price')

#         # Check if quantity or price is not provided
#         if quantity is None or price is None:
#             raise forms.ValidationError("Quantity and price must be provided.")

#         return cleaned_data

# forms.py

#==============================================================================Brand========================================================================== 


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'logo']

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
           
            # Update widget attributes for Bootstrap 5 styling
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
            })

        self.helper = FormHelper()
        self.helper.form_class = 'row g-3'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('description', css_class='col-md-6'),
                Column('logo', css_class='col-md-12'),
                css_class='mb-3'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )
