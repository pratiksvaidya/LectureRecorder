from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

url = 'https://leccap.engin.umich.edu/leccap/'

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

# Login
username = input()
password = input()
username_element = driver.find_element_by_id("login")
password_element = driver.find_element_by_id("password")
username_element.send_keys(username)
password_element.send_keys(password)
driver.find_element_by_id('loginSubmit').click()

# Wait for Two Factor Auth
while (driver.title != 'College of Engineering Lecture Recordings - Available Courses'):
    time.sleep(2)

# Get Courses
soup = BeautifulSoup(driver.page_source, features='html.parser')
classes = soup.find('div', id="recordings").findAll('a')

# Select Course
print('Select course from the list below: ')
for i in range(len(classes)):
    print(str(i+1) + ") " + classes[i].text)
    
course_num = int(input())

course_url = 'https://leccap.engin.umich.edu/' + classes[course_num-1]['href']

driver.get(course_url)

# Get Lectures
soup = BeautifulSoup(driver.page_source, features='html.parser')
classes = soup.find('div', id="recordings").findAll('a')

# Select Lecture
soup = BeautifulSoup(driver.page_source, features='html.parser')
lectures = soup.find('div', id="recordings").findAll('a')
print()
print('Select lecture from the list below: ')
for i in range(len(lectures)):
    print (str(i+1) + ") " + lectures[i]['title'][6:].strip())
    
lecture_num = int(input())

lecture_url = 'https://leccap.engin.umich.edu' + lectures[lecture_num-1]['href']

driver.get(lecture_url)

# Download Lecture
driver.switch_to.window(driver.current_window_handle)
time.sleep(2)

soup = BeautifulSoup(driver.page_source, features='html.parser')
video_url = soup.find('video')['src']
file_name = lectures[lecture_num - 1]['title'][6:].strip() + ".mp4"
urllib.request.urlretrieve("https://" + video_url[2:], file_name)