from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Fayl, Namuna, Sana


def namuna(request):
    link = Namuna.objects.all()
    contex = {
        'link' : link,
    }
    return render(request, 'asosiy/namunalar.html', contex)

def namunalar(request, pk):
    fayl = Namuna.objects.get(id=pk)
    contex = {
        'namunalar' : fayl,
    }
    return render(request, 'asosiy/namunalar.html', contex)



def sana(request):
    vaqt = Sana.objects.all()
    contex = {
        'vaqt' : vaqt,
    }
    return render(request, 'asosiy/fayl.html', contex)

def fayl(request):
    if request.method == 'POST':
        ism = request.POST['ism']
        familya = request.POST['familya']
        fan = request.POST['fan']
        pasport = request.FILES['pasport']
        diplom = request.FILES['diplom']
        ariza = request.FILES['ariza']
        malumotnoma = request.FILES['malumotnoma']
        anketa = request.FILES['anketa']
        kochirma = request.FILES['kochirma']
        yollanma = request.FILES['yollanma']
        royhat = request.FILES['royhat']                              
        fayl =Fayl.objects.create(ism=ism,familya=familya,fan=fan,pasport=pasport,diplom=diplom,ariza=ariza,malumotnoma=malumotnoma,anketa=anketa,kochirma=kochirma,yollanma=yollanma,royhat=royhat)
        fayl.save()
        return redirect('/')
    return render(request, 'asosiy/baza.html')
