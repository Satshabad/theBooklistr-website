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
    
    #### TODO!!!!!! VALIDATE q AND s
    if 'q' in request.GET and request.GET['q']:
        
        # user has not selected a section
        if  not 's' in request.GET:
            sections = [{'name':'E-01',  'instructor':'Gershman',  'section_id':123214}, {'name':'E-02',  'instructor':'Gershman',  'section_id':1234},  {'name':'E-03',  'instructor':'Rich',  'section_id':1214}]
            c = RequestContext(request, {'sections':sections,  'courseid':request.GET['q']})
            return render_to_response('search-selection.html', c)
        ### TODO Do search stuff
        ### QUERY DATABASE USING SECTION ID request.GET['s']and course_id request.GET['q']

        # Test Data
        books = [{'title':'Call of the Wild', 'author':'Jack London', 
                    'ReqOrOpt':'Required','isbn': '0-13-110362-8',  'listings':[]},  {'title':'The C Programming Language', 'author':'Brian W. Kernighan', 
                    'ReqOrOpt':'Required','isbn': '123-456-7890',  'listings':[]}]
        posting = [{'condition':'Great', 'price':'10.00'},  {'condition':'OK', 'price':'13.00'},  {'condition':'Bad', 'price':'100.00'},  {'condition':'Sweet', 'price':'12.00'},  {'condition':'Meh', 'price':'11.00'}]
        books[0]['listings'] = posting
        books[1]['listings'] = posting
                    
        c = RequestContext(request, {'books':books})
               

    elif request.method == 'POST':
        pass
        ### DO BUY STUFF ###

    else:
        c = RequestContext(request)
        return render_to_response('buy.html')
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
