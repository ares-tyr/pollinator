import time
from selenium import webdriver
import qrcode
import getpass
import csv
import variables


driver = webdriver.Chrome(variables.driver_location)
# Optional argument, if not specified will search path.
driver.get('https://www.easypolls.net/')
time.sleep(5)  # Let the user actually see something!
driver.find_element_by_id('OPP-login-logout').click()
email_box = driver.find_element_by_id('OPP-login-email')
email_box.send_keys(input('username please: '))
pw_box = driver.find_element_by_id('OPP-login-password')
pw_box.send_keys(getpass.getpass())
# Search_box.submit()
driver.find_element_by_xpath('/html/body/div[6]/div[11]/div/button[1]/span'
                             ).click()
time.sleep(2)


def create_poll(question_text, choices):
    question_box = driver.find_element_by_id('OPP-question-text')
    question_box.send_keys(question_text)

    for c, choice in enumerate(choices, 1):
        xpath = ("//*[@id='OPP-choice-table'][" + str(c) +
                 "]/tbody/tr[2]/td[1]/input[1]")
        choice_box = driver.find_element_by_xpath(xpath)
        choice_box.send_keys(choice)

    driver.find_element_by_id('OPP-save-poll-button').click()
    time.sleep(2)
    link = driver.find_element_by_xpath('//*[@id="OPP-poll-public-link"]/a'
                                        ).get_attribute('href')
    driver.refresh()
    return link


questions = variables.questions
links = []

for question in questions:
    answers = variables.answers
    links.append(create_poll(question, answers))

print(links)

with open(variables.save_file_location, 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(links)

# TODO make this a function
for c, link in enumerate(links, 1):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,)
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = variables.save_file_location + '/Scenario' + str(c) + '.png'
    img.save(filename)

# TODO make these into variables modules/json files
answers_numbers = variables.questions_2

link_numbers = []

for c, question_numbers in enumerate(answers_numbers, 1):
    question_text = variables.question_2_text + str(c)
    print(question_text)
    print(question_numbers)
    link_numbers.append(create_poll(question_text, question_numbers))

for c, link in enumerate(link_numbers, 1):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,)
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = (variables.save_file_location + '/Scenario' + str(c) +
                '_number.png')
    img.save(filename)

print(link_numbers)

with open(variables.save_file_location + '/link_numbers.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(link_numbers)

driver.quit()
