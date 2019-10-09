from bs4 import BeautifulSoup
from bs4 import Tag
from http.cookiejar import CookieJar
import mechanize
import re
import os

directory = os.path.dirname(os.path.abspath(__file__))

with open(directory + '/config.txt', 'r') as config_file:
    username = config_file.readline().rstrip() # read username
    password = config_file.readline().rstrip() # read password
    ignored_courses = []
    for course in config_file:
        ignored_courses.append(course.rstrip())

cj = CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)

br.open('https://lms.nust.edu.pk/portal/login/index.php')
br.select_form(nr=0)
br.form['username'] = username
br.form['password'] = password # enter username and password into the form
br.submit()

home = br.open('https://lms.nust.edu.pk/portal/my/').read()

soup = BeautifulSoup(home, 'lxml')

current_courses = soup.find('div', {'id': '1'}) # current courses are under div with id 1
required_courses = [] # list for tuples containing course name and link

for course in current_courses.div.contents:
    title = course.h2.a.text
    link = course.h2.a['href']

    title = ' '.join(title.split('  ')) # weird bug with 2 spaces appearing in some titles

    if title not in ignored_courses:
        required_courses.append((title, link))

quotes_regex = re.compile(r'filename="(.*?)"') # regex to get filename from between quotes
size_regex = re.compile(r'Content-Length: (\d+)') # regex to get filesize


def get_file_info(header): # retrieve file size and filename from header
    return size_regex.search(str(header)).group(1), quotes_regex.search(str(header)).group(1)


for title, link in required_courses:

    course_directory = directory + '/' + title

    if not os.path.isdir(course_directory):
        os.mkdir(course_directory)

    print("Currently Downloading from " + title)
    resource_links = []
    course_page = br.open(link).read()
    course_soup = BeautifulSoup(course_page, 'lxml')
    all_weeks = course_soup.find('ul', {'class': 'weeks'}) # no clue why using class_ doesn't work

    for week in all_weeks.contents:
        current_week_list = week.find('ul', {'class': 'section img-text'})
        if current_week_list is not None: # None means there is nothing uploaded for that week
            for element in week.find('ul', class_='section img-text').contents:
                # https://stackoverflow.com/questions/7591535/beautifulsoup-attributeerror-navigablestring-object-has-no-attribute-name
                if isinstance(element, Tag):
                    resource_link = element.find('div', {'class': 'activityinstance'}).a['href']
                    if 'resource' in resource_link:
                        resource_links.append(resource_link)

    for link in resource_links:
        header = br.open(link).info()

        if "Content-Type: text/html" not in str(header): # if the reponse is not an http file...
            size, name = get_file_info(header)
            print("Downloading file: {}".format(name))
            print("Size: {} Bytes".format(size))
            br.retrieve(link, filename=course_directory + '/' + name)

        else:
            resource_file_page = br.open(link).read()
            resource_file_soup = BeautifulSoup(resource_file_page, 'lxml')
            # get the link to the onject embedded in the page
            file_link = resource_file_soup.find('object', {'id': 'resourceobject'})['data']
            header = br.open(file_link).info()
            size, name = get_file_info(header)
            print("Downloading file: {}".format(name))
            print("Size: {} Bytes".format(size))
            br.retrieve(file_link, filename=course_directory + '/' + name)
