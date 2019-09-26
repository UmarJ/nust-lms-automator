from bs4 import BeautifulSoup
from bs4 import Tag
from http.cookiejar import CookieJar
import mechanize

with open('config.txt', 'r') as config_file:
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

for title, link in required_courses:
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
    for i in resource_links:
        print(i)
        downloaded_file = br.open(i).read()
        f = open(i.split('?')[-1], 'wb')
        f.write(downloaded_file)