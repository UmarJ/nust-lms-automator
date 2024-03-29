# Python Standard Library Modules
import re
import os

# Third Party Modules
from bs4 import BeautifulSoup
from bs4 import Tag
from http.cookiejar import CookieJar
import mechanize

# Configuration Data
from config import *

# Set Current Directory as download directory if not specified
if DOWNLOAD_DIRECTORY:
    directory = os.path.expanduser(DOWNLOAD_DIRECTORY)
else:
    directory = os.path.dirname(os.path.abspath(__file__))

cj = CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)

br.open('https://lms.nust.edu.pk/portal/login/index.php')
br.select_form(nr=0)
br.form['username'] = USERNAME
br.form['password'] = PASSWORD
br.submit()

# regex to get filename from between quotes
quotes_regex = re.compile(r'filename="(.*?)"')
# regex to get filesize
size_regex = re.compile(r'Content-Length: (\d+)')
total_files = 0
total_size = 0


# download the file, given the header and directory
def download_file(header, file_link, course_directory):
    size = size_regex.search(str(header)).group(1)
    name = quotes_regex.search(str(header)).group(1)

    lab_directory = os.path.join(
        course_directory, LAB_MANUALS_DIR) if LAB_MANUALS_DIR else None

    # if the file is present in the course directory, nothing needs to be downloaded
    if os.path.isfile(os.path.join(course_directory, name)):
        return

    # if the file is present in the lab directory, nothing needs to be downloaded
    if lab_directory and os.path.isfile(os.path.join(lab_directory, name)):
        return

    full_file_path = os.path.join(course_directory, name)

    if 'lab' in name.lower():
        if lab_directory:
            if not os.path.isdir(lab_directory):
                # create directory for lab manuals if not present
                os.makedirs(lab_directory)
            full_file_path = os.path.join(lab_directory, name)

    global total_files, total_size
    total_files += 1
    total_size += int(size)
    print("Downloading file: {}".format(name))
    print("Size: {} Bytes".format(size))
    br.retrieve(file_link, filename=full_file_path)


for link in COURSE_LINKS:

    course_page = br.open(link).read()
    course_soup = BeautifulSoup(course_page, 'lxml')

    title = course_soup.find('div', class_='page-header-headings').next.next

    if title in ALIASES:
        title = ALIASES[title]

    print("Currently Downloading Course Materials for " + title)
    resource_links = []

    all_weeks = course_soup.find('ul', class_='weeks')

    course_directory = os.path.join(directory, title)
    if not os.path.isdir(course_directory):
        os.makedirs(course_directory)

    for week in all_weeks.contents:
        current_week_list = week.find('ul', class_='section img-text')
        if current_week_list is not None:  # None means there is nothing uploaded for that week
            for element in current_week_list.contents:
                # https://stackoverflow.com/questions/7591535/beautifulsoup-attributeerror-navigablestring-object-has-no-attribute-name
                if isinstance(element, Tag):
                    if 'resource' in element['class']:
                        try:
                            # links that will be available later do not have an anchor tag under div,
                            # although the class is activityinstance, which results in a TypeError when subscripting
                            resource_link = element.find(
                                'div', class_='activityinstance').a['href']
                            if 'resource' in resource_link:
                                resource_links.append(resource_link)
                        except (TypeError, AttributeError):
                            pass

                    elif 'assign' in element['class']:
                        # open assignment page
                        assignment_page = br.open(element.find(
                            'div', class_='activityinstance').a['href']).read()
                        assignment_soup = BeautifulSoup(
                            assignment_page, 'lxml')
                        # check if files have been uploaded to the assignment in the intro div
                        file_upload_divs = assignment_soup.find('div', id='intro').find_all(
                            'div', class_='fileuploadsubmission')
                        for file_upload_div in file_upload_divs:
                            resource_links.append(file_upload_div.a['href'])

    for link in resource_links:
        header = br.open(link).info()

        # if the reponse is not an http file, it means it is the link to a resource that can be downloaded
        if "Content-Type: text/html" not in str(header):
            download_file(header, link, course_directory)
        else:
            resource_file_page = br.open(link).read()
            resource_file_soup = BeautifulSoup(resource_file_page, 'lxml')
            content_div = resource_file_soup.find(
                'div', class_='resourcecontent')

            # resource link may be inside an iframe
            if content_div.find('iframe'):
                file_link = content_div.find('iframe')['src']

            # ...or inside an object embedded in the page (like pdf files)
            elif content_div.find('object'):
                file_link = content_div.find('object')['data']

            # ...or resource may be an image
            elif content_div.find('img'):
                file_link = content_div.find('img')['src']

            else:
                continue

            header = br.open(file_link).info()
            download_file(header, file_link, course_directory)

    print()  # a new line for aesthetic reasons ;)

print("Download Finished. {} new file(s) found.".format(total_files))
print("Total Size: {} Bytes".format(total_size))
