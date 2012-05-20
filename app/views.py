from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import SellBookForm
from forms import ContactSellerForm
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

# include this decorator on all post request view functions
@csrf_protect
def sell(request):
    if request.method == 'POST':
        form = SellBookForm(request.POST)
        if form.is_valid():
            
            # FOR RYAN, INSERT THESE INTO THE DB
            
            isbn = form.cleaned_data['isbn']
            email = form.cleaned_data['email']
            price = form.cleaned_data['price']
            condition = form.cleaned_data['condition']
            
          # Redirect to a confirmation of Book posting page 
            return HttpResponseRedirect('/thanks')
        else:
            return render_to_response('sell.html', RequestContext(request,  {'form':form}))
    form = SellBookForm()

    return render_to_response('sell.html', RequestContext(request,  {'form':form}))

@csrf_protect
def buy(request):
    if 'q' in request.GET and request.GET['q']:
            
        ### TODO Do search stuff
        ### Search query exists in request.GET['q'] ###

        # Test Data
        books = [{'title':'Call of the Wild', 'author':'Jack London', 
                    'ReqOrOpt':'Required','isbn': '0-13-110362-8',  'listings':[]},  {'title':'The C Programming Language', 'author':'Brian W. Kernighan', 
                    'ReqOrOpt':'Required','isbn': '123-456-7890',  'listings':[]}]
        posting = [{'id':'1', 'condition':'Great', 'price':'10.00'},  {'id':'2','condition':'OK', 'price':'13.00'},  {'id':'3','condition':'Bad', 'price':'100.00'},  {'id':'4', 'condition':'Sweet', 'price':'12.00'},  {'id':'5', 'condition':'Meh', 'price':'11.00'}]
        books[0]['listings'] = posting
        books[1]['listings'] = posting
        
        
        form = ContactSellerForm()    
        c = RequestContext(request, {'books':books, 'form':form})
               

    elif request.method == 'POST':
        
        ### TODO Contact Seller Stuff
        ### find the id of the seller with request.POST['id']
        
        
        # Test render_to_response to see if we can get the id of the seller
        return render_to_response('buy.html', {'post_id':request.POST['id']})
        
        # Implement a success page
        #return HttpResponseRedirect('/thanks')

    else:
  
        
        c = RequestContext(request)
        return render_to_response('buy.html', c)
        ### User starts a search ###

    ### TODO Implement form for buy ###
    return render_to_response('buy.html', c)

def contact(request):
    c = RequestContext(request)
    return render_to_response("contact.html", c)

def thanks(request):
    c = RequestContext(request)
    return render_to_response("thanks.html", c)

@csrf_protect
def about(request):
    c = RequestContext(request)
    return render_to_response("about.html", c)

def index(request):
    #send_mail('Subject here', 'Here is the message.', 'from@example.com', ['satshabad.music@gmail.com'], fail_silently=False)
    form = ContactSellerForm()
    c = RequestContext(request, {'form':form})
    return render_to_response("hero.html", c)
