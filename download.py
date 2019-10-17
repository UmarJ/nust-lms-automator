from bs4 import BeautifulSoup
from bs4 import Tag
from http.cookiejar import CookieJar
import mechanize
import re
import os

directory = os.path.dirname(os.path.abspath(__file__))

with open(directory + '/config.txt', 'r') as config_file:
    config_file.readline()
    username = config_file.readline().rstrip() # read username

    config_file.readlines(2)
    password = config_file.readline().rstrip() # read password

    config_file.readlines(2)
    ignored_courses = []
    for line in config_file:
        if line == 'Aliases:\n':
            break
        if line != '\n':
            ignored_courses.append(line.rstrip())

    aliases = {}
    for course in config_file:
        if course == '\n':
            break
        alias = config_file.readline()
        aliases[course.rstrip()] = alias.rstrip()

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

quotes_regex = re.compile(r'filename="(.*?)"') # regex to get filename from between quotes
size_regex = re.compile(r'Content-Length: (\d+)') # regex to get filesize
total_files = 0
total_size = 0


def download_file(header, file_link, course_directory): # download the file, given the header and directory
    size = size_regex.search(str(header)).group(1)
    name = quotes_regex.search(str(header)).group(1)

    if 'lab' in name.lower():
        course_directory += '/Lab Manuals'
        if not os.path.isdir(course_directory): # create Lab Manuals folder if not present
            os.mkdir(course_directory)

    full_file_path = course_directory + '/' + name

    if os.path.isfile(full_file_path): # if the file is already in the folder, nothing needs to be downloaded
        return

    global total_files, total_size
    total_files += 1
    total_size += int(size)
    print("Downloading file: {}".format(name))
    print("Size: {} Bytes".format(size))
    br.retrieve(file_link, filename=full_file_path)


for course in current_courses.div.contents:
    title = course.h2.a.text
    link = course.h2.a['href']

    title = ' '.join(title.split('  ')) # weird bug with 2 spaces appearing in some titles

    if title not in ignored_courses:
        if title in aliases:
            title = aliases[title]
            if title in ignored_courses: # check if the alias is in ignored courses
                continue
        required_courses.append((title, link))

for title, link in required_courses:

    print("Currently Downloading Course Materials for " + title)
    resource_links = []
    course_page = br.open(link).read()
    course_soup = BeautifulSoup(course_page, 'lxml')
    all_weeks = course_soup.find('ul', {'class': 'weeks'}) # no clue why using class_ doesn't work

    course_directory = directory + '/' + title
    if not os.path.isdir(course_directory):
        os.mkdir(course_directory)

    for week in all_weeks.contents:
        current_week_list = week.find('ul', {'class': 'section img-text'})
        if current_week_list is not None: # None means there is nothing uploaded for that week
            for element in week.find('ul', class_='section img-text').contents:
                # https://stackoverflow.com/questions/7591535/beautifulsoup-attributeerror-navigablestring-object-has-no-attribute-name
                if isinstance(element, Tag):
                    try:
                        # links that will be available later do not have an anchor tag under div,
                        # although the class is activityinstance, which results in a TypeError when subscripting
                        resource_link = element.find('div', {'class': 'activityinstance'}).a['href']
                        if 'resource' in resource_link:
                            resource_links.append(resource_link)
                    except TypeError:
                        pass

    for link in resource_links:
        header = br.open(link).info()

        # if the reponse is not an http file, it means it is the link to a resource that can be downloaded
        if "Content-Type: text/html" not in str(header):
            download_file(header, link, course_directory)

        # else a resource file is embedded in the page (probably pdf)
        else:
            resource_file_page = br.open(link).read()
            resource_file_soup = BeautifulSoup(resource_file_page, 'lxml')
            # get the link to the onject embedded in the page
            file_link = resource_file_soup.find('object', {'id': 'resourceobject'})['data']
            header = br.open(file_link).info()
            download_file(header, file_link, course_directory)
    print() # a new line for aesthetic reasons ;)

print("Download Finished. {} new file(s) found.".format(total_files))
print("Total Size: {} Bytes".format(total_size))
