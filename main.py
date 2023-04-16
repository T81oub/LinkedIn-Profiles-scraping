from selenium import webdriver
import time
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import urllib
import pandas as pd
import json
from selenium.webdriver.chrome.service import Service
app = Flask(__name__)
path = r"C:\Users\User\Desktop\chromedriver_win32\chromedriver.exe"


driver = webdriver.Chrome(path)


def login():
    login = open('login.txt') # this is your linkedin account login, store in a seperate text file. I recommend creating a fake account so your real one dosen't get flagged or banned
    line = login.readlines()

    email = line[0]
    password = line[1]

    driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    eml = driver.find_element(by=By.ID, value="username")
    eml.send_keys(email)
    passwd = driver.find_element(by=By.ID, value="password")
    passwd.send_keys(password)
    loginbutton = driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginbutton.click()
    time.sleep(3)


def returnProfileInfo(employeeLink):
    url = employeeLink
    driver.get(url)
    time.sleep(2)
    source = BeautifulSoup(driver.page_source, "html.parser")


    info = source.find('div', class_='mt2 relative')
    profile_name = info.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
    title_description = info.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()

    time.sleep(1)

    URL=driver.current_url
    # Extract education
    education_url = URL + "details/education/"
    driver.get(education_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    education_section = soup.find('section', {'class': 'artdeco-card ember-view pb3'})
    education_section = education_section.find('div', {'class': 'pvs-list__container'})
    education_section = education_section.find('div', {'class': 'scaffold-finite-scroll__content'})
    education_lst = education_section.find_all('li', {
            'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})


    educations = []

    for education in education_lst:
        edu_school = education.find('span', {'class': 'mr1 hoverable-link-text t-bold'}).find('span').text.strip()
        try:
            edu_degree = education.find('span', {'class': 't-14 t-normal'}).find('span').text.strip()
        except:
            edu_degree = 'null'
        try:
            edu_daterange = education.find('span', {'class': 't-14 t-normal t-black--light'}).find('span').text.strip()
        except:
            edu_daterange = 'null'
        educations.append({
            'School': edu_school,
            'Degree': edu_degree,
            'DateRange': edu_daterange
        })

    # Extract work experience
    experience_url = URL + "details/experience/"
    driver.get(experience_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    experience_section = soup.find('div', {'class': 'scaffold-finite-scroll__content'})
    # print(experience_section)
    experience_lst = experience_section.find_all('li', {
        'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
    # print(len(experience_lst))
    experiences = []

    for experience in experience_lst:
        pos_title = experience.find('span', {'class': 'mr1 t-bold'}).find('span').text.strip()
        # print(pos_title)
        pos = experience.find('span', {'class': 't-14 t-normal'}).find('span').text.strip().split("·")
        pos_company=pos[0].strip()
        pos_type= pos[1].strip() if len(pos) > 1 else "null"
        # print(pos_company)
        daterange = experience.find('span', {'class': 't-14 t-normal t-black--light'}).find('span').text.strip().split("·")
        pos_daterange=daterange[0].strip()
        pos_duration=daterange[1].strip() if len(daterange) > 1 else "null"
        try:
            pos_location = experience.find_all('span', {'class': 't-14 t-normal t-black--light'})[1].find(
                'span').text.strip()
            # print(pos_location)
        except:
            pos_location = 'null'

        experiences.append({
            'Title': pos_title,
            'Company': pos_company,
            'Type': pos_type,
            'DateRange': pos_daterange,
            'Duration': pos_duration,
            'Location': pos_location,

        })

    # Extract Skills
    skill_url = URL + "details/skills/"
    driver.get(skill_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    skill_section = soup.find('section', {'class': 'artdeco-card ember-view pb3'})
    skill_section = skill_section.find('div', {'class': 'pvs-list__container'})
    skill_section = skill_section.find('div', {'class': 'scaffold-finite-scroll__content'})
    skill_lst = skill_section.find_all('li', {
        'class': 'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})

    skills = []
    for skill in skill_lst:
        skill_title = skill.find('span', {'class': 'mr1 hoverable-link-text t-bold'}).find('span').text.strip()
        skills.append({
            'Title': skill_title

        })

    return jsonify({
        'Name': profile_name,
        'Title': title_description,
        'Skill': skills,
        'Experience': experiences,
        'Education': educations
    })
login()
@app.route('/employee', methods=['POST'])
def return_profile_info():



    employee_link = request.json.get('employee_link')
    return returnProfileInfo(employee_link)

if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
