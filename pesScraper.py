import selenium
import time
from selenium import webdriver

# Use Chrome to access web
k = int(input('Max Limit (usually not more than 2000): '))
br = input('Branch (CS, EC, EE, ME, CV, BT): ')
chrome = webdriver.Chrome('/bin/chromedriver')

# Create an empty (for now) database to store students
studentDatabase = []

for num in range (1,k):
    # Generate the current ID
    i = str(num).zfill(3)
    ID = 'PES1UG19' + br + i
    IDsimp = br+i
    # Open the website
    chrome.get('https://pesuacademy.com/Academy/')
    
    # Find the Know your Class & Section button and click it
    class_section_button = chrome.find_element_by_xpath(r'//*[@id="knowClsSection"]')
    class_section_button.click()
    
    # Find the form in which you enter the SRN
    SRN = chrome.find_element_by_xpath(r'//*[@id="knowClsSectionModalLoginId"]')
    time.sleep(0.4)
    
    # Enter the current ID
    SRN.send_keys(ID)
    
    # Find the Search button and click it
    search_button = chrome.find_element_by_xpath(r'//*[@id="knowClsSectionModalSearch"]')
    search_button.click()
    time.sleep(0.4)
    
    # If the number is valid, find and store the Name element in the table shown, to the variable 'name'
    try:
        name = chrome.find_element_by_xpath(r'//*[@id="knowClsSectionModalTableDate"]/tr/td[3]').text
    
    # If an exception (error) is thrown, assign a blank space to all variables
    except:
        name = ''
        section = ''
        branch = ''
    
    # If an exception was not thrown, find and store the Section and Branch elements in the table shown, the the variables 'section' and 'branch'
    else:
        section = chrome.find_element_by_xpath(r'//*[@id="knowClsSectionModalTableDate"]/tr/td[5]').text
        branch = chrome.find_element_by_xpath(r'//*[@id="knowClsSectionModalTableDate"]/tr/td[8]').text
    
    # Create a list called 'student' containing the scraped data
    student = [IDsimp, name, section, branch]
    
    # Add this student to the Database
    studentDatabase.append(student)

# Write all the Students in the Database to a file
with open ("thing.txt", 'r') as pesStudents:
    text = pesStudents.read()
    for student in studentDatabase:
        for num in range (1,k):
            i = str(num).zfill(3)
            Id = br + i
            if student[0] == Id:
                text = text.replace(Id, student[1] + ' ' + student[2])
                print(Id, student[0], student[1])
with open ("thing.txt", 'w') as f:
    f.write(text)
    """for item in student:
        pesStudents.write("%s, " % item)
    pesStudents.write("\n")"""
