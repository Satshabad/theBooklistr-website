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
            
            # NOW GENERATE SECRET KEY and PUBLIC KEY
            # Redirect to a confirmation of Book posting page 
            return HttpResponseRedirect('/thanks?key=123&postnumber=456')
        else:
            return render_to_response('sell.html', RequestContext(request,  {'form':form}))
    form = SellBookForm()

    return render_to_response('sell.html', RequestContext(request,  {'form':form}))

def contact(request):
    c = RequestContext(request)
    return render_to_response("contact.html", c)

def thanks(request):
    c = RequestContext(request,  {'secretkey':request.GET['key'], 'postnumber':request.GET['postnum'] })
    return render_to_response("thanks.html", c)

@csrf_protect
def about(request):
    c = RequestContext(request)
    return render_to_response("about.html", c)

def index(request):
    form = ContactSellerForm()
    c = RequestContext(request, {'form':form})
    return render_to_response("hero.html", c)

@csrf_protect
def search(request):

    if request.method == "GET":
        # The user has submitted a get request
        
        if  's' in request.GET and 'q' in request.GET:
            # The user has selected a course and a section. Send the book listings
            
             # TEST DATA. USE QUERIES INSTEAD HERE
             books = [{'title':'Call of the Wild', 'author':'Jack London', 
                    'ReqOrOpt':'Required','isbn': '0-13-110362-8',  'listings':[]},  {'title':'The C Programming Language', 'author':'Brian W. Kernighan', 
                    'ReqOrOpt':'Required','isbn': '123-456-7890',  'listings':[]}]
             posting = [{'id':'1', 'condition':'Great', 'price':'10.00'},  {'id':'2','condition':'OK', 'price':'13.00'},  {'id':'3','condition':'Bad', 'price':'100.00'},  {'id':'4', 'condition':'Sweet', 'price':'12.00'},  {'id':'5', 'condition':'Meh', 'price':'11.00'}]
             books[0]['listings'] = posting
             books[1]['listings'] = posting
            # end test data
        
             # return the search results and a form for them to contact the seller
             form = ContactSellerForm()    
             c = RequestContext(request, {'books':books, 'form':form})
             return render_to_response('search.html', c)
            
            
        elif  'q' in request.GET and request.GET['q']:
            # The user has only selected a course. Send the section listings. Unless q is empty.
            
            # TEST DATA. USE QUERIES INSTEAD HERE
            sections = [{'name':'E-01',  'instructor':'Gershman',  'section_id':123214}, {'name':'E-02',  'instructor':'Gershman',  'section_id':1234},  {'name':'E-03',  'instructor':'Rich',  'section_id':1214}]
            # end test data
            
            # pass the section to the user and the course they selected so it can passed back to us later
            c = RequestContext(request, {'sections':sections,  'coursename':request.GET['q']})
            return render_to_response('search-selection.html', c)
            
            
        else:
            # The user has not submitted any relevent data, or no data. Render a default search page.
            return render_to_response('search.html')
        
def contactseller(request):
    
    if request.method == "POST":
        # The user has submitted a post request
        
        if  not 'postid' in request.POST:
            # if they did not submit a postid, which is automatic, then just redirect them to the home page.
            return HttpResponseRedirect('/search')
            
        form = ContactSellerForm(request.POST)
        if form.is_valid():
            
            
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            
           ### TODO Contact Seller Stuff
           #send_mail('Subject here', 'Here is the message.', 'from@example.com', ['satshabad.music@gmail.com'], fail_silently=False)
        
        # Implement a success page
        #return HttpResponseRedirect('/thanks')
        else:
            return render_to_response('contactseller.html', RequestContext(request,  {'form':form, 'postid': request.POST['postid']}))
            
    if request.method == "GET":
        if  not 'postid' in request.GET:
            # if they did not submit a postid, which is automatic, then just redirect them to the home page.
            return HttpResponseRedirect('/search')
            
        form = ContactSellerForm() 
        c = RequestContext(request,  {'form':form,  'postid':request.GET['postid']})
        return render_to_response("contactseller.html", c)
        
    
    
   
       
        
        
        
        
        
