from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import time
import datetime

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

washer_data = set()
raw_html = simple_get("https://www.laundryalert.com/cgi-bin/STAN9568/LMRoom?XallingPage=LMPage&Halls=73&PreviousHalls=&RoomPersistence=&MachinePersistenceA=&MachinePersistenceB=")
html = BeautifulSoup(raw_html, 'html.parser')
for table in html.select('table'):
    if(table.has_attr('background') and table['background'] == "/images/images_halls/white_blue_bg.gif"):
        for colored_text in table.select("font"):
            washer_data.add(colored_text.text.strip())

num_washers = 0
num_dryers = 0
for element in washer_data:
    if("dryers" in element):
        num_dryers = element.split(' ')[0]
    elif("washers" in element):
        num_washers = element.split(' ')[0]

with open('washer_drier_data.csv', 'a') as data_storage:
    data_storage.write("{},{},{}\n".format(num_washers, num_dryers, datetime.datetime.today()))
