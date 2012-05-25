from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import SellBookForm
from forms import ContactSellerForm
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from models import ListedBook
from models import Book
from models import Section
import random
import urllib

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.template.loader import get_template

from django import template
from django.template import Context
import re
import string

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
            
            # A random 16 digit hex number
            secretKey = ''.join(random.choice(string.hexdigits) for n in xrange(16))
            
            listing = ListedBook(
                secret_key = secretKey,
                isbn = form_isbn,
                email = form_email,
                price = form_price,
                condition = form_condition)
            secretKey = str(secretKey)
            # insert the new listing into the database
            listing.save()
            html_content = render_to_string('successpostingemail.html', {'deleteLink':'www.thebooklistr.com/delete?s='+secretKey})
            text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

            msg = EmailMultiAlternatives('Your book has been posted', text_content, 'noreply@theBooklistr.com', [form_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
         
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
        message = 'Sorry, that did not compute'
        if 's' in request.GET:


            isValid = False
            # a little trick here. If the list is not empty then at
            # least one of the charaters in s is not hex.
            if len(request.GET['s']) == 16 and not [x for x in request.GET['s'] if not x in string.hexdigits]:
                isValid = True

            if isValid:
                try:

                    toDelete = ListedBook.objects.get(secret_key=request.GET['s'])
                    toDelete.delete()
                    title = 'Post deleted'
                    message = 'Thank you, please come back soon'

                except ListedBook.DoesNotExist:
                    pass


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

            #  retrieve the list of books that correspond to a Course and Section
            #correctBooks = Section.objects.filter(courseName = request.GET['q'])

            # VALIDATE
            if re.match(r'^\w{1,5}\s*\d{3}$', request.GET['q']) is None \
                or re.match(r'^\d{1,30}$', request.GET['s']) is None:
                # The user has submitted an irregular section id or course name
                return render_to_response('search.html')

            books2 = Book.objects.filter(sectionID=request.GET['s'])

            returnBooks = []
            for dbBook in books2:
                newBook = {'title':dbBook.title, 'author':dbBook.author, 'isRequired':dbBook.required, 'isbn':dbBook.isbn, 'listings':[]}
                listings = ListedBook.objects.filter(isbn=newBook['isbn'])
                newBook['listings'] = listings
                returnBooks.append(newBook)


            # go through the list of books and find the listings


            # TEST DATA. USE QUERIES INSTEAD HERE
 #           books = [{'title':'Call of the Wild', 'author':'Jack London',
#                    'ReqOrOpt':'Required','isbn': '0-13-110362-8',  'listings':[]},  {'title':'The C Programming Language', 'author':'Brian W. Kernighan',
  #                  'ReqOrOpt':'Required','isbn': '123-456-7890',  'listings':[]}]
#            posting = [{'id':'1', 'condition':'Great', 'price':'10.00'},  {'id':'2','condition':'OK', 'price':'13.00'},  {'id':'3','condition':'Bad', 'price':'100.00'},  {'id':'4', 'condition':'Sweet', 'price':'12.00'},  {'id':'5', 'condition':'Meh', 'price':'11.00'}]
           # books[0]['listings'] = posting
           # books[1]['listings'] = posting


            # HERE WE LOOK UP THE AMAZON PAGE AND PRICE FOR EACH BOOK
            amazon = bottlenose.Amazon(AMAZON_API_KEY, AMAZON_SECRET_KEY,  AMAZON_ASSOC_TAG )

            for book in returnBooks:
                # Do this for each book.
                book['amazon'] = {}
                response = amazon.ItemLookup(ItemId=book['isbn'].replace('-', ''), ResponseGroup="ItemAttributes, Offers ",SearchIndex="Books", IdType="ISBN")
                soup = BeautifulSoup.BeautifulSoup(response)


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
            c = RequestContext(request, {'books':returnBooks, 'form':form})

            #c = RequestContext(request, {'books' : correctBooks, 'form' : form})
            return render_to_response('search.html', c)

		#############
        # The user has only entered a courseName (i.e. CS240)
        #   -- List the sections of that course
		#############
        elif  'q' in request.GET and request.GET['q']:

            # VALIDATE
            if re.match(r'^\w{1,5}\s*\d{3}$', request.GET['q']) is None:
                # The user has submitted an irregular course name
                return render_to_response('search.html')

            # query the database for the courses with the name requested in q
            sections = Section.objects.filter(courseName = request.GET['q'])

            # pass the section to the user and the course they selected
            # so it can passed back to us later

            c = RequestContext(request, {'sections' : sections, 'coursename':request.GET['q']})
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
            html_content = render_to_string('contactselleremail.html', {'message':message, 'email': email})
            text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
            listing = ListedBook.objects.filter(id=request.POST['postid'])

            msg = EmailMultiAlternatives('Someone from Booklistr wants to by your book', text_content, 'noreply@theBooklistr.com', [listing[0].email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
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
