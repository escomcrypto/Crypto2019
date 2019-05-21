from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app.models import PaintingRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/signin.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
    
#In this view a list of requests that the user has made will be shown
def ordersList(request):
    orders=[]
    #result = PaintingRequest.objects.filter(username=request.user.id).values()
    result = PaintingRequest.objects.filter(username="mayrasho").values()
    if(len(result)!=0):
        for r in range(0,len(result)):
            orders.append(result[r]['name'])
    else:
        print("No hay pedidos")
    return render(request, 'requestsClient.html', 
        {
            'orders':orders,
            'title':'Orders',
            'year':datetime.now().year,
        }
    )


#def contact(request):
#    """Renders the contact page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/contact.html',
#        {
#            'title':'Contact',
#            'message':'Your contact page.',
#            'year':datetime.now().year,
#        }
#    )

#def about(request):
#    """Renders the about page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/about.html',
#        {
#            'title':'About',
#            'message':'Your application description page.',
#            'year':datetime.now().year,
#        }
#    )
