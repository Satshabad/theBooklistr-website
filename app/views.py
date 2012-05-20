from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import SellBookForm
from forms import ContactSellerForm
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from models import ListedBook
from models import Course

# for amazon calls
from amazonify import amazonify
import BeautifulSoup
import bottlenose

AMAZON_API_KEY = 'AKIAI75ZQQCZ726SSJDA'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = 'books0ae3-20'

# include this decorator on all post request view functions
@csrf_protect
def sell(request):
    if request.method == 'POST':
        form = SellBookForm(request.POST)
        if form.is_valid():
            form_isbn = form.cleaned_data['isbn']
            form_email = form.cleaned_data['email']
            form_price = form.cleaned_data['price']
            form_condition = form.cleaned_data['condition']

            # NOW GENERATE SECRET KEY and SEND TO USER IN EMAIL 
            # in the form http://oururl.com/delete?id_email=usersencodedemail&id_secret. 
            #   Clicking this link will delete their post
            #send_mail('Subject here', 'Here is the message.', 'from@example.com', 
            #   ['satshabad.music@gmail.com'], fail_silently=False)
            secret_key = '1';

            listing = ListedBook(private_id = secret_key, isbn = form_isbn, email = form_email, price = form_price, condition = form_condition)

            # insert the new listing into the database
            listing.save()
            
            # NOW GENERATE SECRET KEY and SEND TO USER IN EMAIL in the form http://oururl.com/delete?id_email=usersencodedemail&id_secret. Clicking this link will delete their post
            message = '''Hey there book seller,
            
            Your book with isbn: '''+isbn+''' is posting to Books at $'''+price+''', people will now be able to see it and we'll send you their email if they want to get in touch with you.
            
            Clicking this link will delete your posting.
            <a href="http://oururl.com/delete?id_email=usersencodedemail&id_secret=123>Don't click this unless you mean it' </a>
            
            Thanks, The Books Team
            
            '''
            #send_mail('Your book has been posted', message, 'noreply@Books.com', ['satshabad.music@gmail.com'], fail_silently=False)

            # Redirect to a confirmation of Book posting page 
            return HttpResponseRedirect('/thanks')
        else:
            return render_to_response('sell.html', RequestContext(request,  {'form':form}))
    form = SellBookForm()

    return render_to_response('sell.html', RequestContext(request,  {'form':form}))

def thanks(request):
    pagename = 'Thank you'
    title = 'Thanks for your listing'
    message = 'It should be posted in a just a few minutes. An email has been sent to you.'
    c = RequestContext(request, {'pagename':pagename, 'title':title,  'message':message} )
    return render_to_response("titleandmessage.html", c)
    
def messageSent(request):
    pagename = 'Message Sent'
    title = 'Your message has been sent'
    message = 'The seller now has your email address and may contact you'
    c = RequestContext(request, { 'pagename':pagename, 'title':title,  'message':message} )
    return render_to_response("titleandmessage.html", c)

def delete(request):
    if request.method == 'GET':
        pagename = 'Delete Post'
        title = 'Uh Oh'
        message = 'Sorry that did not compute'
        if 'secret' in request.GET and 'email' in request.GET:
            
            # DO DATA VALIDATION HERE
            if True:
                
                # DELETE USERS POST HERE, MAKE SURE IT's IN DB, if not use error message
                 
                 title = 'Post deleted'
                 message = 'Thank you, please come back soon'
                
                
        c = RequestContext(request, {'pagename':pagename, 'title':title,  'message':message})
        return render_to_response("titleandmessage.html", c)
            
        
        

@csrf_protect
def search(request):

    # The user has submitted a get request
    if request.method == "GET":

		#############
        # The user has selected a course and a section. 
		# - Provide the books that are listed for that course and section.
		#############
        if  's' in request.GET and 'q' in request.GET:
            courses = Course.objects.filter(name = request.GET['q'])

            #  retrieve the list of books that correspond to a Course and Section
            correctBooks = Course.objects.filter(name = request.GET['q'], sectionID = request.GET['s'])
           
            # TEST DATA. USE QUERIES INSTEAD HERE
            books = [{'title':'Call of the Wild', 'author':'Jack London', 
                    'ReqOrOpt':'Required','isbn': '0-13-110362-8',  'listings':[]},  {'title':'The C Programming Language', 'author':'Brian W. Kernighan', 
                    'ReqOrOpt':'Required','isbn': '123-456-7890',  'listings':[]}]
            posting = [{'id':'1', 'condition':'Great', 'price':'10.00'},  {'id':'2','condition':'OK', 'price':'13.00'},  {'id':'3','condition':'Bad', 'price':'100.00'},  {'id':'4', 'condition':'Sweet', 'price':'12.00'},  {'id':'5', 'condition':'Meh', 'price':'11.00'}]
            books[0]['listings'] = posting
            books[1]['listings'] = posting

             
            # HERE WE LOOK UP THE AMAZON PAGE AND PRICE FOR EACH BOOK
            amazon = bottlenose.Amazon(AMAZON_API_KEY, AMAZON_SECRET_KEY,  AMAZON_ASSOC_TAG )

            for book in books:
                # Do this for each book. 
                book['amazon'] = {}
                response = amazon.ItemLookup(ItemId=book['isbn'].replace('-', ''), ResponseGroup="ItemAttributes, Offers ",SearchIndex="Books", IdType="ISBN")
                soup = BeautifulSoup.BeautifulSoup(response)
                print book['isbn'].strip('-')
                 
                # check to see that response exists
                if not soup.find('items').findAll('item'):
                    continue
                     
                for item in soup.find('items').findAll('item'):
                    if not(item.find('detailpageurl') and item.find('lowestusedprice') and item.find('lowestnewprice')):
                        continue
                    link = item.find('detailpageurl').text
                    reflink = amazonify(link,  AMAZON_ASSOC_TAG)
                    book['amazon']['link'] = reflink
                    usedprice = item.find('lowestusedprice').find('formattedprice').text
                    book['amazon']['usedprice'] = usedprice
                    newprice = item.find('lowestnewprice').find('formattedprice').text
                    book['amazon']['newprice'] = newprice
            # end test data

            
        
            # return the search results and a form for them to contact the seller
            form = ContactSellerForm()    
            c = RequestContext(request, {'books':books, 'form':form})
            return render_to_response('search.html', c)

		#############
        # The user has only entered a courseName (i.e. CS240)
        #   -- List the sections of that course
		#############
        elif  'q' in request.GET and request.GET['q']:

            # query the database for the courses with the name requested in q
            courses = Course.objects.filter(name = request.GET['q'])

            # TEST DATA. USE QUERIES INSTEAD HERE
            #sections = [{'name':'E-01',  'instructor':'Gershman',  'section_id':123214}, {'name':'E-02',  'instructor':'Gershman',  'section_id':1234},  {'name':'E-03',  'instructor':'Rich',  'section_id':1214}]
            # end test data
            
            # pass the section to the user and the course they selected 
            # so it can passed back to us later
            #c = RequestContext(request, {'sections':sections,  'coursename':request.GET['q']})
            c = RequestContext(request, {'courses' : courses})
            return render_to_response('search-selection.html', c)
            
        else:
            # The user has not submitted any relevent data, or no data. 
            # - Render a default search page.
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
            return HttpResponseRedirect('/message')
        else:
            return render_to_response('contactseller.html', RequestContext(request,  {'form':form, 'postid': request.POST['postid']}))
            
    if request.method == "GET":
        if  not 'postid' in request.GET:
            # if they did not submit a postid, which is automatic, then just redirect them to the home page.
            return HttpResponseRedirect('/search')
            
        form = ContactSellerForm() 
        c = RequestContext(request,  {'form':form,  'postid':request.GET['postid']})
        return render_to_response("contactseller.html", c)
