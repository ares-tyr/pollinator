import time
from selenium import webdriver
import qrcode
import getpass
import csv


driver = webdriver.Chrome('C:/Users/lujame1/Documents/chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://www.easypolls.net/');
time.sleep(5) # Let the user actually see something!
driver.find_element_by_id('OPP-login-logout').click()
email_box = driver.find_element_by_id('OPP-login-email')
email_box.send_keys(getpass.getuser)
pw_box = driver.find_element_by_id('OPP-login-password')
pw_box.send_keys(getpass.getpass())
#search_box.submit()
driver.find_element_by_xpath('/html/body/div[6]/div[11]/div/button[1]/span').click()
time.sleep(2)

def create_poll(question_text, choices):
    question_box = driver.find_element_by_id('OPP-question-text')
    question_box.send_keys(question_text)

    for c, choice in enumerate(choices, 1):
        xpath = "//*[@id='OPP-choice-table'][" + str(c) + "]/tbody/tr[2]/td[1]/input[1]"
        choice_box = driver.find_element_by_xpath(xpath)
        choice_box.send_keys(choice)

    driver.find_element_by_id('OPP-save-poll-button').click()
    time.sleep(2)
    link = driver.find_element_by_xpath('//*[@id="OPP-poll-public-link"]/a').get_attribute('href')
    driver.refresh()
    return link


questions = ['Scenario 1', 'Scenario 2', 'Scenario 3', 'Scenario 4', 'Scenario 5', 'Scenario 6', 'Scenario 7', 'Scenario 8', 'Scenario 9', 'Scenario 10', 'Scenario 11']
links = []

for question in questions:
    answers = ['Increase', 'Flat', 'Decrease']
    links.append(create_poll(question, answers))

print(links)

with open('Y:/Code/Automation/images/links_master.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(links)

# TODO make this a function
for c, link in enumerate(links,1):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,)
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = 'Y:/Code/Automation/images/Scenario' + str(c) + '.png'
    img.save(filename)

# TODO make these into variables modules/json files
answers_numbers = [
    ['+0%','+1.5%','-1.5%'],
    ['-5.6%','-2.5%','-7.1%'],
    ['+5.6%','+2.5%','+7.1%'],
    ['-2.2%','-2.5%','-2%'],
    ['+2.2%','+2.5%','+2%'],
    ['+7.5%','+5%','+2.5%'],
    ['-8.3%','-11%','-2%'],
    ['-18.4%','-14.4%','-16.4%'],
    ['+21%','+3.6%','+25%'],
    ['+3.8%','+20%','+2.7%'],
    ['-17.4%','-20%','-3.2%']]

link_numbers = []

for c, question_numbers in enumerate(answers_numbers, 1):
    question_text = 'What is the rate change in Scenario ' + str(c)
    print(question_text)
    print(question_numbers)
    link_numbers.append(create_poll(question_text, question_numbers))

for c, link in enumerate(link_numbers,1):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,)
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = 'Y:/Code/Automation/images/Scenario' + str(c) + '_number.png'
    img.save(filename)

print(link_numbers)

with open('Y:/Code/Automation/images/link_numbers.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(link_numbers)

driver.quit()