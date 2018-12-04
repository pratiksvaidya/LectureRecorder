from __future__ import print_function

import sys
import time
import urllib.request

from getpass import getpass

from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

from constants import BASE_URL
from utils import print_info, print_warning, print_error, print_success


def initialize():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(BASE_URL)

    return driver

def login(driver):
    username = input('Enter UM username: ')
    password = getpass('Enter UM password: ')

    print_info("\nLogging in...")

    username_element = driver.find_element_by_id("login")
    password_element = driver.find_element_by_id("password")
    username_element.send_keys(username)
    password_element.send_keys(password)
    driver.find_element_by_id('loginSubmit').click()

    if driver.find_element_by_id('title').text == "Two-Factor Authentication Required":
        # Wait for Two Factor Auth
        print_warning("Please accept 2FA authentication request.\n")
        while driver.title != 'College of Engineering Lecture Recordings - Available Courses':
            time.sleep(2)

def get_classes(driver):
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    return soup.find('div', id="recordings").findAll('a')

def select_class(classes):
    for i, course in enumerate(classes):
        print(str(i+1) + ") " + course.text)

    course_num = input('\nSelect course from the list above: ')
    while not validate_num_input(len(classes), course_num):
        print_error('Your input is invalid.')
        course_num = input('Please enter a number between 1 and ' + str(len(classes)) + ': ')

    return 'https://leccap.engin.umich.edu/' + classes[int(course_num)-1]['href']

def get_lectures(driver, course_url):
    driver.get(course_url)
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    lectures = soup.find('div', id="recordings").findAll('a')
    if not lectures:
        print_error('There are no lectures recorded for this class.')
        sys.exit()

    return lectures

def select_lecture(driver, lectures):
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    lectures = soup.find('div', id="recordings").findAll('a')
    print()
    for i, lecture in enumerate(lectures):
        print (str(i+1) + ") " + lecture['title'][6:].strip())

    lecture_num = input('\nSelect lecture from the list above: ')
    while not validate_num_input(len(lectures), lecture_num):
        print_error('Your input is invalid.')
        lecture_num = input('Please enter a number between 1 and ' + str(len(lectures)) + ': ')

    url = 'https://leccap.engin.umich.edu' + lectures[int(lecture_num)-1]['href']
    title = lectures[int(lecture_num) - 1]['title'][6:].strip()
    return (url, title)

def download_lecture(driver, url, title):
    driver.get(url)
    driver.switch_to.window(driver.current_window_handle)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, features='html.parser')
    video_url = soup.find('video')['src']

    file_name = title + ".mp4"
    print_info('\nDownloading ' + file_name + " ...")
    if '/' in file_name:
        file_name = file_name.replace('/', '-')

    urllib.request.urlretrieve("https://" + video_url[2:], file_name)
    print_success('Download Complete!')
    driver.quit()

def validate_num_input(list_size, usr_input):
    if usr_input == '':
        return False
    elif usr_input.lower() == 'quit':
        sys.exit()

    try:
        val = int(usr_input)
        if val <= 0 or val > list_size:
            return False
        return True
    except ValueError:
        return False

def main():
    driver = initialize()
    login(driver)
    classes = get_classes(driver)

    course_url = select_class(classes)
    lectures = get_lectures(driver, course_url)

    lecture_url, lecture_title = select_lecture(driver, lectures)
    download_lecture(driver, lecture_url, lecture_title)

if __name__ == '__main__':
    main()
