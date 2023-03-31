from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Fayl

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
        Fayl.objects.create(ism=ism,familya=familya,fan=fan,pasport=pasport,diplom=diplom,ariza=ariza,malumotnoma=malumotnoma,anketa=anketa,kochirma=kochirma,yollanma=yollanma,royhat=royhat)
        return redirect('/files/')
    return render(request, 'asosiy/fayl.html')

def yuklash(request):
    fayl = Fayl.objects.all
    context = {
        'data':fayl,
    }
    return render(request, 'asosiy/yuklash.html', context)


