from bs4 import BeautifulSoup
import getpass
import selenium.webdriver as webdriver
import sys
import time
import urllib.request


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

url = 'https://leccap.engin.umich.edu/leccap/'

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

def validate_num_input(list_size, input):
    if input == '':
        return False
    elif input.lower() == 'quit':
        sys.exit()

    try:
        val = int(input)
        if val <= 0 or val > list_size:
            return False
        return True
    except ValueError:
        return False

# Login
print('Enter UM username: ', end = '')
username = input()
password = getpass.getpass('Enter UM password: ')

print("\nLogging in...")

username_element = driver.find_element_by_id("login")
password_element = driver.find_element_by_id("password")
username_element.send_keys(username)
password_element.send_keys(password)
driver.find_element_by_id('loginSubmit').click()

if driver.find_element_by_id('title').text == "Two-Factor Authentication Required":
    # Wait for Two Factor Auth
    print("Please accept 2FA authentication request.\n")
    while (driver.title != 'College of Engineering Lecture Recordings - Available Courses'):
        time.sleep(2)

# Get Courses
soup = BeautifulSoup(driver.page_source, features='html.parser')
classes = soup.find('div', id="recordings").findAll('a')

# Select Course
for i in range(len(classes)):
    print(str(i+1) + ") " + classes[i].text)
    
print('\nSelect course from the list above: ', end = '')
course_num = input()
while not (validate_num_input(len(classes), course_num)):
    print('Your input is invalid. Please enter a number between 1 and ' + str(len(classes)) + ': ' , end = '')
    course_num = input()

course_url = 'https://leccap.engin.umich.edu/' + classes[int(course_num)-1]['href']

driver.get(course_url)

# Get Lectures
soup = BeautifulSoup(driver.page_source, features='html.parser')
classes = soup.find('div', id="recordings").findAll('a')
if len(classes) == 0:
    print('There are no lectures recorded for this class.')
    sys.exit()

# Select Lecture
soup = BeautifulSoup(driver.page_source, features='html.parser')
lectures = soup.find('div', id="recordings").findAll('a')
print()
for i in range(len(lectures)):
    print (str(i+1) + ") " + lectures[i]['title'][6:].strip())

print('\nSelect lecture from the list above: ', end = '')
lecture_num = input()
while not (validate_num_input(len(lectures), lecture_num)):
    print('Your input is invalid. Please enter a number between 1 and ' + str(len(lectures)) + ': ' , end = '')
    lecture_num = input()

lecture_url = 'https://leccap.engin.umich.edu' + lectures[int(lecture_num)-1]['href']

driver.get(lecture_url)

# Download Lecture
driver.switch_to.window(driver.current_window_handle)
time.sleep(2)

soup = BeautifulSoup(driver.page_source, features='html.parser')
video_url = soup.find('video')['src']

file_name = lectures[int(lecture_num) - 1]['title'][6:].strip() + ".mp4"
print('\nDownloading ' + file_name + " ...")
if '/' in file_name:
    file_name = file_name.replace('/', '-')

urllib.request.urlretrieve("https://" + video_url[2:], file_name)
print('Download Complete!')
driver.quit()
