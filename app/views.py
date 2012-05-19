from django.shortcuts import render_to_response
from django.template import RequestContext
from SellBookForm.forms import SellBookForm



def sell(request):
  if request.method == 'POST':
    form = SellBookForm(request.POST)
    if form.is_valid():
      cd = form.cleand_data()
      
      ### DO STUFF ###
      
      # Redirect to a confirmation of Book posting page 
      return HttpResponseRedirect('/some/url')
  
  else:
    form = SellBookForm()

  return render_to_response('sell.html', {'form':form})




def index(request):
    c = RequestContext(request, {'var_name':"Allen"})
    return render_to_response("buy.html", c)
