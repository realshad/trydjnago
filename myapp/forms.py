from django.forms import ModelForm
from .models import Product
from django import forms

class MyProductModelForm(ModelForm):
    title=forms.CharField(required=False,label='Product Title :', widget=forms.TextInput(
                                attrs={"width": "25 %", "placeholder": "Title of the product"}))
    description = forms.CharField(required=False)
    price = forms.DecimalField
    class Meta:
        model = Product
        fields = ['title', 'description', 'price']


class ProductDjangoForm(forms.Form):
    title       = forms.CharField(label='Product Title :', widget=forms.TextInput(attrs={"width": "100 %", "placeholder" : "your title"}))
    description = forms.CharField()
    price       = forms.DecimalField()

class ProductFormValidateForm(forms.ModelForm):
    title 	= forms.CharField(label='Title :', widget=forms.TextInput(attrs={"width": "100 %", "placeholder" : "your title"}))
    test = forms.TextInput()
    description = forms.CharField(widget=forms.Textarea(
                                    attrs={"placeholder" : "your Description ",
                                            "id" : "Desc",
                                            "rows" : 10,
                                            "cols" : 50,
                                           "class": "fieldRequired",
                                           "required": True,
                                           "width": "100 %"
                                           }
                                ))
    price = forms.DecimalField(initial=199.00)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price']

    def clean_title(self, *args, **kwargs):   # syntax for filed validate is clean_<fildName>
        title = self.cleaned_data.get("title")
        print('title :', title)
        if  'CFE' is title:
            print('inside :', title)
            raise forms.ValidationError("title is not correct value")
        if  "ABC" is title:
            raise forms.ValidationError("title is not correct value")
        return title
    """
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if email.endwith("edu"):
            raise forms.ValidationError("Email is not correct value")
        return email
    """
    # form widgets example
    Search_fields = ['prod_id', 'Desc', 'Test_id']

BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]

class SimpleForm(forms.Form):
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )
