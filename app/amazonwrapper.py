# for amazon calls
from amazonify import amazonify
import BeautifulSoup
import bottlenose

AMAZON_API_KEY = 'AKIAI75ZQQCZ726SSJDA'
AMAZON_SECRET_KEY = 'blah'
AMAZON_ASSOC_TAG = 'books0ae3-20'

def getBookInfoByIsbn(isbn):
    '''
    This function takes an string (with "-"'s is ok) isbn and gives back a python dict with
    link: the link to the book at amazon.com, with our assoc tag ;)
    usedprice: the used price
    newprice: the new price

    if no book info is found, an empty dict is returned
    '''

    # HERE WE LOOK UP THE AMAZON PAGE AND PRICE FOR EACH BOOK
    amazon = bottlenose.Amazon(AMAZON_API_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

    bookInfo = {}

    response = amazon.ItemLookup(ItemId=isbn.replace('-', ''),
        ResponseGroup="ItemAttributes, Offers ", SearchIndex="Books", IdType="ISBN")
    soup = BeautifulSoup.BeautifulSoup(response)


    # check to see that response exists, if not just return {}
    if not soup.find('items').findAll('item'):
        return bookInfo

    for item in soup.find('items').findAll('item'):
        if not(item.find('detailpageurl') and item.find('lowestusedprice') and item.find('lowestnewprice')):
            continue
        link = item.find('detailpageurl').text
        reflink = amazonify(link, AMAZON_ASSOC_TAG)
        bookInfo['link'] = reflink
        usedprice = item.find('lowestusedprice').find('formattedprice').text
        bookInfo['usedprice'] = usedprice
        newprice = item.find('lowestnewprice').find('formattedprice').text
        bookInfo['newprice'] = newprice

    return bookInfo
