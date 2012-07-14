from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import SellBookForm
from forms import ContactSellerForm
from forms import FeedbackForm
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from models import ListedBook
from models import Book
from models import Section
import amazonwrapper
import random

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import re
import string

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
                secret_key=secretKey,
                isbn=form_isbn,
                email=form_email,
                price=form_price,
                condition=form_condition)
            secretKey = str(secretKey)
            # insert the new listing into the database
            listing.save()
            html_content = render_to_string('successpostingemail.html',
                    {'deleteLink': 'www.thebooklistr.com'+reverse('delete')+'?s=' + secretKey})
            text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

            msg = EmailMultiAlternatives('Your book has been posted', text_content, 'noreply@theBooklistr.com',
                [form_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('thanks')

        else:
            feedbackform = FeedbackForm()
            return render_to_response('sell.html', RequestContext(request, {'form': form, 'feedbackform':feedbackform}))
    form = SellBookForm()
    feedbackform = FeedbackForm()
    return render_to_response('sell.html', RequestContext(request, {'form': form, 'feedbackform':feedbackform}))


def thanks(request):
    pagename = 'Thank you'
    title = 'Thanks for your listing'
    message = 'It should be posted in a just a few minutes. An email has been sent to you.'
    feedbackform = FeedbackForm()
    c = RequestContext(request, {'pagename': pagename, 'title': title, 'message': message, 'feedbackform':feedbackform})
    return render_to_response("titleandmessage.html", c)


def messageSent(request):
    pagename = 'Message Sent'
    title = 'Your message has been sent'
    message = 'The seller now has your email address and may contact you'
    feedbackform = FeedbackForm()
    c = RequestContext(request, {'pagename': pagename, 'title': title, 'message': message, 'feedbackform':feedbackform})
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
        feedbackform  = FeedbackForm()
        c = RequestContext(request, {'pagename': pagename, 'title': title, 'message': message, 'feedbackform':feedbackform})
        return render_to_response("titleandmessage.html", c)




@csrf_protect
def search(request):

    # The user has submitted a get request
    if request.method == "GET":

        # The user has selected a course and a section.
        # - Provide the books that are listed for that course and section.
        if  'param_sectionID' in request.GET and 'param_coursename' in request.GET:
            return _search_full_results_page(request)

        # The user has only entered a courseName (i.e. CS240)
        #   -- List the sections of that course
        elif  'param_coursename' in request.GET and request.GET['param_coursename']:
            return _search_section_results_page(request)

        # The user has not submitted any relevent data, or no data.
        # - Render a default search page.
        else:
            feedbackform = FeedbackForm()
            return render_to_response('search.html', {'feedbackform': feedbackform})

def _search_full_results_page(request):
    feedbackform = FeedbackForm()
    '''
    This is a helper function to render the full results page. It should be called only when user has provided:
    'param_coursename' and 'param_sectionID'
    '''
    #  retrieve the list of books that correspond to a Course and Section
    #correctBooks = Section.objects.filter(courseName = request.GET['param_coursename'])

    # VALIDATE

    m = re.match(r'^[a-zA-Z]{1,5}\d{3}$', request.GET['param_coursename'])

    if m is None or re.match(r'^\d{1,30}$', request.GET['param_sectionID']) is None:
        # The user has submitted an irregular section id or course name
        message = "Sorry, we couldn't find what you were looking for."
        c = RequestContext(request, {'message': message})
        return render_to_response('search.html', c)

    # go through the list of books and find the listings
    books2 = Book.objects.filter(sectionID=request.GET['param_sectionID'])

    returnBooks = []
    for dbBook in books2:
        newBook = {'title': dbBook.title, 'author': dbBook.author, 'isRequired': dbBook.required,
                   'isbn': dbBook.isbn, 'listings': []}
        listings = ListedBook.objects.filter(isbn=newBook['isbn'])
        newBook['listings'] = listings
        returnBooks.append(newBook)

    # get the amazon info for the books

    for book in returnBooks:
        book['amazon'] = amazonwrapper.getBookInfoByIsbn(book['isbn'])

    # Provide the user a message if this course has no textbooks
    if not returnBooks:
        message = "The textbooks for this section could not be found. " \
            + "The instructor for this course may not have submitted a " \
            + "textbook request yet, or may not be using a text. Please check back later."
    else:
        message = ""

    # return the search results and a form for them to contact the seller
    form = ContactSellerForm()
    c = RequestContext(request, {'books': returnBooks, 'form': form, 'feedbackform':feedbackform, 'message':message})

    #c = RequestContext(request, {'books' : correctBooks, 'form' : form})
    return render_to_response('search.html', c)

def _search_section_results_page(request):
    feedbackform = FeedbackForm()

    # VALIDATE

    if re.match(r'^[a-zA-Z]{1,5}\d{3}$', request.GET['param_coursename']) is None:
        # The user has submitted an irregular section id or course name
        message = "Sorry, we couldn't find what you were looking for."
        c = RequestContext(request, {'message': message})
        return render_to_response('search.html', c)

    # get an object like [{'quarterName': u'SUMMER 2012'}, {'quarterName': u'FALL 2012'}] to have all the quarter names in them
    quarters = list(Section.objects.values('quarterName').distinct())

    # put all the courses in their approprtate quarter contatiners. We get : [{'courses': [<Section: Section object>, <Section: Section object>],
    #'quarterName': u'SUMMER 2012'},{'courses': [<Section: Section object>], 'quarterName': u'FALL 2012'}]
    for quarter in quarters:
        quarter['sections'] = Section.objects.filter(courseName=request.GET['param_coursename'],
            quarterName=quarter['quarterName'])

    # pass the section to the user and the course they selected
    # so it can passed back to us later
    c = RequestContext(request, {'quarters': quarters, 'coursename': request.GET['param_coursename'], 'feedbackform':feedbackform})
    return render_to_response('search-section-selection.html', c)

def contactseller(request):
    if request.method == "POST":
        # The user has submitted a post request

        if  not 'postid' in request.POST:
            # if they did not submit a postid, which is automatic, then just redirect them to the home page.
            return redirect('search')

        form = ContactSellerForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            html_content = render_to_string('contactselleremail.html', {'message': message, 'email': email})
            text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
            listing = ListedBook.objects.filter(id=request.POST['postid'])

            msg = EmailMultiAlternatives('Someone from Booklistr wants to by your book', text_content,
                'noreply@theBooklistr.com', [listing[0].email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('message')
        else:
            return render_to_response('contactseller.html',
                RequestContext(request, {'form': form, 'postid': request.POST['postid']}))

    if request.method == "GET":
        if  not 'postid' in request.GET:
            # if they did not submit a postid, which is automatic, then just redirect them to the home page.
            return redirect('search')

        form = ContactSellerForm()
        feedbackform = FeedbackForm()
        c = RequestContext(request, {'form': form, 'postid': request.GET['postid'],'feedbackform':feedbackform})
        return render_to_response("contactseller.html", c)


def goog(request):
    return render_to_response("google906daeabdf21c107.html", {})

def feedback(request):
    feedbackform = FeedbackForm(request.POST)
    if not feedbackform.is_valid():
        return redirect('search')
    else:
        message = feedbackform.cleaned_data['message']
        email = feedbackform.cleaned_data['email']
        send_mail('feedback', message, email, ['satshabad@thebooklistr.com'], fail_silently=True)
        return redirect('feedbackThanks')

def feedbackThanks(request):
    pagename = 'Feedback Sent'
    title = 'Your feedback has been sent'
    message = 'Thanks for your input, we\'ll get back to you soon.'
    return render_to_response("titleandmessage.html", {'pagename': pagename, 'title': title, 'message': message})
