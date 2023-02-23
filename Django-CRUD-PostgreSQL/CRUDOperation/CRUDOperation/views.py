from django.shortcuts import render, redirect

from CRUDOperation.models import IhaModel, CategoryModel, UserModel

from django.contrib import messages

from CRUDOperation.forms import IhaForms

# Birden fazla kolon için search ve multi_q özelliğini kullanmamız için için projeye dahil ettik
from django.db.models import Q


# kullanıcının giriş yapıp yapmadığını kontrol eden fonksiyon
# kullanıcıların giriş yapmadan sadece register(kayı ol) sayfasına yönlendirmemiz için register ve login hariç tüm sayfalara
#  girmesini önlemek için sayfaya yönlendirilen tüm fonksiyoların başınada bu kontrolü yapıyoruz
def loginControl(request):

        try:
            request.session['user']
            return True
        except Exception:
            return False


# ihaların tüm listesini veya arama kutusundaki değerlere göre değer döndern ve index sayfasına yönlediren fonksiyon
def showIha(request):

    # kullanıcı giriş yapmamış ise Login sayfasına Yönlendir
    if  not loginControl(request)   :
        return redirect('/Login')



    # arama kutusundaki değer için arama yapan ve ona göre data dönderen blok
    if 'q' in request.GET:
        q = request.GET['q']

        try:
            kategori = CategoryModel.objects.filter(kategori__icontains=q)
        except CategoryModel.DoesNotExist:
            kategori = None

        multiple_q = Q(Q(marka__icontains=q) | Q(model__icontains=q) | Q(agirlik__icontains=q) | Q(kategori__in=kategori))

        data = IhaModel.objects.filter(multiple_q)
    elif 'f' in request.GET:
        f = request.GET['f']

        try:
            kategori = CategoryModel.objects.filter(kategori__icontains=f)
        except CategoryModel.DoesNotExist:
            kategori = None

        multiple_f = Q(Q(kategori__in=kategori))

        data = IhaModel.objects.filter(multiple_f)
    else:
        data = IhaModel.objects.all()

    kategoridata = CategoryModel.objects.all()
    return render(request, 'Index.html', {"data": data, "kategoridata": kategoridata})

def filterCategory(request):    

    if 'f' in request.GET:
        f = request.GET['f']

        try:
            kategori = CategoryModel.objects.filter(kategori__icontains=f)
        except CategoryModel.DoesNotExist:
            kategori = None

        multiple_f = Q(Q(kategori__in=kategori))

        data = IhaModel.objects.filter(multiple_f)

    else:

        data = IhaModel.objects.all()

    kategoridata = CategoryModel.objects.all()
   
    return render(request, 'Index.html', {"data": data, "kategoridata": kategoridata})


def insertCategory(request):
    if  not loginControl(request):
        return redirect('/Login')   
    

        
    if request.method == "POST":

        if request.POST.get('kategori')  :
            

            # kategoriler tablosunda gelen kategori değeri yok ise işlem yapar
            # aynı kategoride birden fazla kayıt eklememek için
            if CategoryModel.objects.filter(kategori = request.POST.get('kategori')).count() == 0:
                model = CategoryModel()
                model.kategori = request.POST.get('kategori')
                model.save()
                messages.success(request, ' '+' Başarıyla kaydedildi...!')
                return render(request, 'InsertCategory.html')
            else :
                messages.success(request, 'Bu kategori zaten var !!!')
                return render(request, 'InsertCategory.html')
    else:
        return render(request, 'InsertCategory.html')


def insertIha(request):
    if  not loginControl(request)   :
        return redirect('/Login')

    kategoridata = CategoryModel.objects.all()
    if request.method == "POST":
        if request.POST.get('marka') and request.POST.get('model') and request.POST.get('agirlik') and request.POST.get('kategori'):
            saverecord = IhaModel()
            saverecord.marka = request.POST.get('marka')
            saverecord.model = request.POST.get('model')
            saverecord.agirlik = request.POST.get('agirlik')
            saverecord.kategori =  CategoryModel.objects.get(id=request.POST.get('kategori'))
            saverecord.save()
            messages.success(request, ' ' + saverecord.marka +
                             ' Başarıyla kaydedildi...!')
            return render(request, 'InsertIha.html', {"kategoridata": kategoridata})
    else:
        return render(request, 'InsertIha.html', {"kategoridata": kategoridata})


def register(request):

    if request.method == "POST":
        if request.POST.get('name') and request.POST.get('lastname') and request.POST.get('email') and request.POST.get('password'):
            kullanicilar = UserModel.objects.filter(email=request.POST.get('email'))
            # kullanıcı veritabanında var mı  ?
            if kullanicilar.count() == 0:
                saverecord = UserModel()
                saverecord.adi = request.POST.get('name')
                saverecord.soyadi = request.POST.get('lastname')
                saverecord.email = request.POST.get('email')
                saverecord.sifre = request.POST.get('password')

                saverecord.save()
                messages.success(
                    request, ' ' + saverecord.email + ' Başarıyla kaydedildi...!')

                return redirect("/Login")
            else:
                
                messages.success(
                    request, request.POST.get('email')+' Bu Kullanıcı Zaten var !!! ')
                return render(request, 'Register.html')

    else:
        return render(request, 'Register.html')


def login(request):
    if request.method == "POST":
        if request.POST.get('email') and request.POST.get('password'):
            kullanicilar = UserModel.objects.filter(email = request.POST.get('email') , sifre =request.POST.get('password') )
            # kullanıcı veritabanında var mı  ?
            if kullanicilar.count() != 0:
                request.session['user'] = 'Geldi'            

                return redirect("/")
            else:
                messages.success(request, ' Kullanıcı veya şifre hatalı..!')
                return render(request, 'Login.html')
                
    else:
        messages.success(request,'')

        return render(request, 'Login.html')

def logout(request):
    try:

        del request.session['user']
    except:
        pass

    return redirect('/Login')




def editIha(request, id):
    if  not loginControl(request)   :
        return redirect('/Login')
    editihaobj = IhaModel.objects.get(id=id)
    kategoridata = CategoryModel.objects.all()
    return render(request, 'Edit.html', {"IhaModel": editihaobj, "kategoridata": kategoridata})


def updateIha(request, id):
    if  not loginControl(request)   :
        return redirect('/Login')
    updateiha = IhaModel.objects.get(id=id)
    form = IhaForms(request.POST, instance=updateiha)
    if form.is_valid():
        form.save()
        messages.success(request, ' '+updateiha.marka +
                         ' Başarıyla Güncellendi...!')

        return render(request, 'Edit.html', {"IhaModel": updateiha})


def delIha(request, id):
    if  not loginControl(request)   :
        return redirect('/Login')
    delihaa = IhaModel.objects.get(id=id)
    delihaa.delete()
    return redirect("/")

def delCategory(request, id):
    if  not loginControl(request)   :
        return redirect('/Login')
    
    delCategoryy = CategoryModel.objects.get(id=id)
    delCategoryy.delete()
    C.objects.filter(b__a__c=200).delete()
    return redirect("/")
