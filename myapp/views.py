from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, departments1
from .forms import (MyProductModelForm, ProductDjangoForm, ProductFormValidateForm)
from django.shortcuts import render_to_response
from .mycalc import InterestRage

# Create your views here.

def homepage(request):
    return HttpResponse('<h1> Hello Jango, THis is project batch</h1>')

def homehtml(request):
    return render(request, 'homepage.html',{})

def BootStrap(request):
    return render(request, 'BootStrapTest.html',{})

def rawHtml(request):
    my_contant = {
        "my-text": "This is Abount Us",
        "my_number": 123,
        "my_list": [123, 234, 234]
    }
    return render(request, 'myapp/RawHtmlRender.html', my_contant )


def product_Rawcreate_view(request):
    my_title = request.POST.get('title')
    p_description = request.POST.get('description')
    p_price = request.POST.get('price')
    print('price', p_price)

    if request.method == 'POST':
        Product.objects.create(title=my_title, description=p_description,
                               price=p_price, summary="default sumary" )  ## this will post data ro database
    return render(request, "myapp/prod_raw_create.html", {})

def Product_object_list_view(request):
    queryset = Product.objects.all()
    queryset1 = departments1.objects.all()
    contaxt = {
        "objectList": queryset,
        "DeptDtls": queryset1,
    }
    return render(request, "myapp/prod_list.html", contaxt)

def Product_update_view(request, **kwargs):

    my_id = kwargs.get("my_id")
    print('my_id', my_id, request.method)
    if request.method == 'POST':
        my_title = request.POST.get('title')
        p_description = request.POST.get('description')
        p_price = request.POST.get('price')
        print('my_id', my_id)
        Product.objects.filter(id=my_id).update(title=my_title, description=p_description,price=p_price, summary="default sumary" )

    if request.method == 'GET':
        obj = get_object_or_404(Product, id=my_id)
        #obj = Product.objects.get(id=my_id)
        contaxt = {
                "prod" : obj
            }
        return render(request, "myapp/prod_raw_update.html", contaxt)

    return render(request, "myapp/prod_raw_update.html", {})

def product_delete_view(request, my_id):
    print('my_id :', my_id)
    obj = get_object_or_404(Product, id=my_id)
    #obj.delete() # this will delete without confirmation
    if request.method == 'POST':  #if user submit for Delete (POST) object will delete
        obj.delete()
    print('title', obj.title)
    contaxt = {
    "obj" : obj
    }

    return render(request, "myapp/Prod_raw_delete.html", contaxt)

# Django Model form
def prod_ModelForm_create_view(request):
    form = MyProductModelForm(request.POST)
    if form.is_valid():
        #form.save()
        instance = form.save(commit=False)
        print(instance.title)
        instance.save()
        form = MyProductModelForm()
    contaxt = {
        'form': form
    }
    return render(request, "myapp/Prod_ModelForm_Create.html", contaxt)

def prod_ModelForm_CRUD_view(request):
    pmessage = ''
    calcValue = 0
    OperationAllowed = 'Create'
    form = MyProductModelForm()
    if request.method == 'GET':
        search_id = request.GET.get('Sid')
        print('search_id', search_id)
        if request.GET.get('Sid') != "None" :
            try:
                session = Product.objects.get(id=request.GET.get('Sid'))
                form = MyProductModelForm(instance=session)
                OperationAllowed='UD'
            except Product.DoesNotExist:
                form = MyProductModelForm()
                contaxt = {
                    'form': form,
                    'message' : "Entered Invalid Id"
                }
                return render(request, "myapp/prod_ModelForm_crud_Operations.html", contaxt)

    if request.method in ['POST']:
        if 'Delete' in request.POST :

            #session = Product.objects.get(title=request.POST.get('title')) # if title match with multiple records it throws error
            session=Product.objects.filter(title=request.POST.get('title'))  # if title match with multiple records it return  and delete
            session.delete()
            pmessage = "Record Deleted.."
            form = MyProductModelForm()

        elif 'Create' in request.POST:
            form = MyProductModelForm(request.POST)
            print('form', form)
            if form.is_valid():
                form.save()
                pmessage="Data Saved....."
                form = MyProductModelForm()
        elif 'Update' in request.POST:
            session = Product.objects.get(id=request.GET.get('Sid'))
            form = MyProductModelForm(request.POST, instance=session)
            if form.is_valid():
                print('udpate form', form)
                form.save()
                print('form.cleaned_data', form.cleaned_data)
                pmessage = "Data Updated....."
                form = MyProductModelForm()
        elif 'Calc' in request.POST:
            session = Product.objects.get(id=request.GET.get('Sid'))
            form = MyProductModelForm(request.POST, instance=session)
            if form.is_valid():
                calcValue =  InterestRage(100000,12,2)

    print('calcValue', calcValue)
    print('OperationAllowed', OperationAllowed)
    contaxt = {
        'form': form,
        'pmessage' : pmessage,
        'calcValue' : calcValue,
        'OperationAllowed' : OperationAllowed
    }
    return render(request, "myapp/prod_ModelForm_crud_Operations.html", contaxt)

def ProductDjangoForm_view(request):

    if request.method == 'POST':  # if method is POST validate the for data
        my_form = ProductDjangoForm(request.POST)
        if my_form.is_valid():  # if the form is having valid data post data to Database
            print('formdata Data', my_form)
            print('cleanrd Data', my_form.cleaned_data)
            Product.objects.create(**my_form.cleaned_data)

        else:
            print(my_form.errors)

    context = {
        'form': my_form
    }
    return render(request, 'myapp/Prod_PureDjangoFormCreate.html', context)

def ProductDjangoForm_CRUD_view(request):
    pmessage = ''
    calcValue = 0
    OperationAllowed = 'Create'
    if request.method == 'GET':
        search_id = request.GET.get('Sid')
        if search_id != 'None':
            try:
                session = Product.objects.get(id=request.GET.get('Sid'))
                my_form = ProductDjangoForm({'id': session.id,
                                            'title' : session.title,
                                             'description' : session.description,
                                             'price': session.price
                                             })
                OperationAllowed = 'UD'
                print('formdata', my_form)
            except Product.DoesNotExist:
                my_form = ProductDjangoForm()
                print('form', my_form)
                contaxt = {
                    'form': my_form,
                    'message': "Entered Invalid Id"
                }
                return render(request, "myapp/Prod_PureDjangoForm_CRUD.html", contaxt)

    if request.method in ['POST']:
        if 'Create' in request.POST :
            if my_form.is_valid():  # if the form is having valid data post data to Database
                print('cleaned Data', my_form.cleaned_data)
                Product.objects.create(**my_form.cleaned_data)
                pmessage="Record Inserted.."
            else:
                my_form = ProductDjangoForm()
                print(my_form.errors)
        elif 'Update' in request.POST:
            my_form = MyProductModelForm(request.POST)
            print('Update Request')
            if my_form.is_valid():
                Product.objects.filter(id=request.GET.get('Sid')).update(title=my_form.data.get('title'),\
                                                                         description=my_form.data.get('description'),
                                                                         price=my_form.data.get('price')
                                                                         )

            my_form = ProductDjangoForm()
            pmessage = "Record Updated.."
        elif 'Delete' in request.POST:
            my_form = ProductDjangoForm(request.POST)
            if my_form.is_valid():
                print('del', my_form.data)
                obj = get_object_or_404(Product, id=request.GET.get('Sid'))
                obj.delete()
                pmessage="Record Deleted.."
            my_form = ProductDjangoForm()

    context = {
        'form': my_form,
        'OperationAllowed':OperationAllowed,
        'pmessage': pmessage
    }
    return render(request, 'myapp/Prod_PureDjangoForm_CRUD.html', context)

def caluate_view(request):
    p = 0
    r = 0
    t = 0
    cal_val = 0

    print(request.POST)
    if request.method in ['POST']:
        if 'Calc' in request.POST :
            print('datatype', type(request.POST.get('Price')))
            p = request.POST.get('Price')
            r = request.POST.get('Rate')
            t = request.POST.get('Time')
            cal_val = InterestRage(int(p), int(t), float(r))

            print('cal_val1', cal_val)
        elif 'save' in request.POST:
            p = request.POST.get('Price')
            r = request.POST.get('Rate')
            t = request.POST.get('Time')
            cal_val = InterestRage(int(p), int(t), float(r))
            #prt.objects.create(p,t,r,cal_val)
            print('calc values Before Rein', p,t,r,cal_val)
            p = 0
            r = 0
            t = 0
            cal_val = 0

    context = {
        'p': p,
        'r': r,
        't': t,
        'cal_val': cal_val
    }

    return render(request, 'myapp/InterestCalculations.html', context)
