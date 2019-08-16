from django.shortcuts import render
from .forms import CommentForm, cars_model_form, ChoiceForm,ProductFormValidateForm,FormValidateTest
from .models import Car
# Create your views here.

def FormWidgets_view(request):
    form = CommentForm(request.POST)
    #print(form)
    if form.is_valid():
        print('is valid')
        form.save()
        form = CommentForm()
    contaxt = {
        'form': form
    }

    return render(request, "FormWidgets/FormWidgets.html", contaxt)

def CarsModelForm_view(request):
    form = cars_model_form(request.POST, request.FILES)
    print('formdata', form)
    print('file', request.FILES)
    if form.is_valid():
        print('is valid')
        form.save_m2m()
        form = CommentForm()
    contaxt = {
        'form': form
    }

    return render(request, "FormWidgets/Media.html", contaxt)

def CarsModelFormDisplay_view(request):
    obj = Car.objects.all()
    contaxt = {
        'obj': obj
    }

    return render(request, "FormWidgets/CarMOdelDetails.html", contaxt)

def ChoiceForm_view(request):
    form = ChoiceForm()
    if form.is_valid():
        form.save_m2m()
        form = CommentForm()
    contaxt = {
        'form': form
    }
    return render(request, "FormWidgets/ChoiceField.html", contaxt)


def ProductFormValidate_view(request):
    form = ProductFormValidateForm(request.POST)
    print(form)
    if form.is_valid():
        print('is valid')
        form.save()
        form = ProductFormValidateForm()

    contaxt = {
        'form': form
    }

    return render(request, "FormWidgets/Product_Create_formValidate.html", contaxt)

def FormValidateTest_view(request):
    form = FormValidateTest()
    if request.method == 'POST':
        form = FormValidateTest(request.POST)

    if form.is_valid():
        print('formdata', form.cleaned_data)
        form.clean()
        form.save()
        form = FormValidateTest()

    contaxt = {
        'form': form
    }

    return render(request, "FormWidgets/Product_Create_formValidate.html", contaxt)