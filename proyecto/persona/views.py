from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from persona.models import Pedido

#Method that allows you to login given the username and password
def inicioSesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('persona:main')
        messages.add_message(request, messages.INFO,'Incorrect user and/or password.')
    return render(request, 'InicioSesion.html')

#This view shows the welcome
def main(request):
    return render(request, 'main.html')

#In this view a list of orders that the user has made will be shown
def ordersList(request):
    orders=[]
    result = Pedido.objects.filter(username=request.user.id).values()
    if(len(result)!=0):
        for r in range(0,len(result)):
            orders.append(result[r]['name'])
    else:
        print("No hay pedidos")
    return render(request, 'orders.html', {'orders':orders})
