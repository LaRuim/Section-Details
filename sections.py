from utilities import selenium_utils, log
import time, datetime

# Use Chrome to access web
def scrape(branch, Campus, startYear):

    chrome = selenium_utils.make_driver()
    load = selenium_utils.load(chrome)  

    # Create an empty (for now) database to store students
    studentDatabase = []
    failCount = 0
    numberID = 1

    while True:
        # Generate the current SRN
        if failCount > 3:
            break
        ID = str(numberID).zfill(3)
        SRN = f'PES{Campus}UG{startYear}{branch}{ID}'

        # Open the website
        chrome.get('https://pesuacademy.com/Academy/')
        
        # Find the Know your Class & Section button and click it
        load(r'//*[@id="knowClsSection"]', 'xpath').click()
        
        # Find the form in which you enter the SRN and enter the current SRN
        form = load(r'//*[@id="knowClsSectionModalLoginId"]', 'xpath')
        time.sleep(0.4)
        form.send_keys(SRN)
        
        # Find the Search button and click it
        load(r'//*[@id="knowClsSectionModalSearch"]', 'xpath').click()
        
        # If the number is valid, find and store the Name element in the table shown, to the variable 'name'
        try:
            name = load(r'//*[@id="knowClsSectionModalTableDate"]/tr/td[3]', 'xpath').text
        
        # If an exception (error) is thrown, assign a blank space to all variables
        except:
            name = ''
            section = ''
            campus = ''
            failCount += 1
        
        # If an exception was not thrown, find and store the Section and Campus elements in the table shown, the the variables 'section' and 'campus'
        else:
            section = load(r'//*[@id="knowClsSectionModalTableDate"]/tr/td[5]', 'xpath').text
            campus = load(r'//*[@id="knowClsSectionModalTableDate"]/tr/td[9]', 'xpath').text
            failCount = 0
        
        # Create a list called 'student' containing the scraped data
        student = [SRN, name, section, campus]
        log.info(', '.join(student))

        # Add this student to the Database
        studentDatabase.append(student)
        numberID += 1

    # Write all the Students in the Database to a file
    with open (f"{branch} Section Details.csv", 'w+') as sectionDetailsFile:
        for student in studentDatabase:
            if student.count('') > 2:
                continue
            line = ', '.join(student)
            sectionDetailsFile.write(line)
            sectionDetailsFile.write("\n")


def main():
    startYear = input('Year of first semester (20xx): ')
    currentYear = datetime.datetime.now().year
    if len(startYear) == 4:
        if int(startYear) > currentYear:
            log.error(f"Can't really time-travel.. {startYear}, really o.O?")
            return
        else:
            startYear = startYear[2:]
    elif len(startYear) == 2:
        if int(startYear) > int(str(currentYear)[2:]):
            log.error(f"Can't really time-travel.. {startYear}, really o.O?")
            return
    else:
        log.error(f'What kind of year is {startYear} o.O?')
        return
    branch = input('Branch (CS, EC, EE, ME, CV, BT): ').upper()
    if branch not in ['CS', 'EC', 'EE', 'ME', 'CV', 'BT']:
        log.error(f'Branch {branch} does not exist or is not supported')
        return
    campus = input('Campus (RR or EC): ').upper()
    if campus not in ['RR', 'EC']:
        log.error(f'Campus {campus} does not exist or is not supported')
        return
    campus = 1 if campus == 'RR' else 2

    scrape(branch=branch, Campus=campus, startYear=startYear)


if __name__ == '__main__':
    main()