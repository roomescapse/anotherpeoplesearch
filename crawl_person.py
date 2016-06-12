import time
import re
import urllib2
import Queue
from bs4 import BeautifulSoup
import json

PREFIX = 'https://people.us.oracle.com/pls/oracle/'

def parse_single_person(soup):
    key_list = ['Work Phone:', 'Work Email:', 'Address:', 'Building:',
    'Organization:', 'Floor:', 'Office', 'Cost Center:', 'Directs ', 'Total ',
    'Manager:','Global UID:', 'Job Title:', 'Manager Level:']
    person_info = {}

    for key in key_list:
        table_data = soup.find('td', text=re.compile(key))
        if table_data:
            person_info[key] = table_data.find_next_sibling().get_text()
    return json.dumps(person_info)

def parse_all(queue, f):
    html = urllib2.urlopen(queue.get()).read()
    soup = BeautifulSoup(html, 'html.parser')
    f.write(parse_single_person(soup) + '\n')
    
    directs = soup.find('td', text=re.compile('Directs '))
    if directs:
        for link in directs.find_next_sibling().find_all('a'):
            queue.put(PREFIX + link.get('href'))

def run():
    html = 'https://people.us.oracle.com/pls/oracle/f?p=8000:2:::::PERSON_ID:443509209820316'
    parse_queue = Queue.Queue()
    parse_queue.put(html)
    file_name = 'people.txt'
    with open(file_name, 'w') as f:
        while not parse_queue.empty():
            parse_all(parse_queue, f)

start_time = time.time()
run()
end_time = time.time()
print end_time - start_time 
