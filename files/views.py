from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Fayl, Namuna, Sana


@csrf_exempt
def namuna(request):
    link = Namuna.objects.all()
    contex = {
        'link' : link,
    }
    return render(request, 'asosiy/namunalar.html', contex)

# def namunalar(request, pk):
#     fayl = Namuna.objects.get(id=pk)
#     contex = {
#         'namunalar' : fayl,
#     }
#     return render(request, 'asosiy/namunalar.html', contex)

@csrf_exempt
def javob(request, pk):
    fayl = Fayl.objects.get(id=pk)
    contex = {
        'javob':fayl,
    }
    return render(request, 'asosiy/hujjatlar.html', contex)

@csrf_exempt
def sana(request):
    vaqt = Sana.objects.all()
    contex = {
        'vaqt' : vaqt,
    }
    return render(request, 'asosiy/fayl.html', contex)

@csrf_exempt
def fayl(request):
    habar = ''
    if request.method == 'POST':
        ism = request.POST['ism']
        familya = request.POST['familya']
        telefon = request.POST['telefon']
        fan = request.POST['fan']
        pasport = request.FILES['pasport']
        diplom = request.FILES['diplom']
        ariza = request.FILES['ariza']
        malumotnoma = request.FILES['malumotnoma']
        anketa = request.FILES['anketa']
        kochirma = request.FILES['kochirma']
        royhat = request.FILES['royhat']                              
        fayl =Fayl.objects.create(ism=ism,familya=familya,telefon=telefon, fan=fan,pasport=pasport,diplom=diplom,ariza=ariza,malumotnoma=malumotnoma,anketa=anketa,kochirma=kochirma,royhat=royhat)
        fayl.save()
        habar = 'Muvaffaqiyatli qo`shildi !!! '
        return render(request, 'asosiy/home.html', {
            'habar':habar,
        })
    return render(request, 'asosiy/baza.html')
