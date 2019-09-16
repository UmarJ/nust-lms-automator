from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import mechanize

config_file = open('config.txt')
username = config_file.readline().rstrip()
password = config_file.readline()

cj = CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)

br.open('https://lms.nust.edu.pk/portal/login/index.php')
br.select_form(nr=0)
br.form['username'] = username
br.form['password'] = password
br.submit()

home = br.open('https://lms.nust.edu.pk/portal/my/').read()

soup = BeautifulSoup(home, 'lxml')
print(soup.prettify())