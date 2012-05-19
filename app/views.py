from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import SellBookForm
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect

# include this decorator on all post request view functions
@csrf_protect
def sell(request):
    if request.method == 'POST':
        form = SellBookForm(request.POST)
        if form.is_valid():
            cd = form.cleand_data()
          
        # DO STUFF ###
          
          # Redirect to a confirmation of Book posting page 
            return HttpResponseRedirect('/thanks.html')
        else:
            print 'here'
            return render_to_response('sell.html', RequestContext(request,  {'form':form}))
    form = SellBookForm()

    return render_to_response('sell.html', RequestContext(request,  {'form':form}))

@csrf_protect
def buy(request):
    if request.method == 'GET':
        pass    
        ### DO SEARCH STUFF ####

    elif request.method == 'POST':
        pass
        ### DO BUY STUFF ###

    else:
        pass
        ### User starts a search ###

    ### TODO Implement form for search and buy ###
    return render_to_response('buy.html')

def contact(request):
    c = RequestContext(request)
    return render_to_response("contact.html", c)

@csrf_protect
def about(request):
    c = RequestContext(request)
    return render_to_response("about.html", c)

def index(request):
    c = RequestContext(request)
    return render_to_response("hero.html", c)
