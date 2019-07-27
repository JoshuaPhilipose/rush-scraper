from selenium import webdriver
import time
import pandas as pd


def main():
    data = pd.read_csv('names.csv')
    emails = []

    # Open up site in selenium
    driver = webdriver.Chrome(executable_path='C:/chromedriver.exe')
    driver.get('https://www.directory.gatech.edu/')

    for index, row in data.iterrows():
        fName = row["First Name"]
        lName = row["Last Name"]

        email = scraper(fName, lName, driver)
        emails.append(email)

    data["Email Address"] = emails
    data.to_csv('namesAndEmails.csv',index=False)

def scraper(fName, lName, driver):

    # Find elements
    fNameInput = driver.find_element_by_id("edit-firstname")
    lNameInput = driver.find_element_by_id("edit-lastname")
    captchaProblem = driver.find_element_by_xpath('//*[@id="edit-captcha"]/div/div[2]/label').get_attribute('innerHTML')
    captchaInput = driver.find_element_by_id("edit-captcha-test")
    submit = driver.find_element_by_id("edit-submit")

    # send information
    fNameInput.send_keys(fName)
    lNameInput.send_keys(lName)

    solution = solver(captchaProblem)
    captchaInput.send_keys(solution)

    submit.click()
    # time.sleep(1)

    try:
        driver.find_element_by_xpath('//*[@id="block-system-main"]/div/p/a').click()
    except:
        print("No entry found for " + fName + " " + lName)
        return "No entry found"
    # time.sleep(1)
    email = driver.find_element_by_xpath('//*[@id="block-system-main"]/div/p[1]/a').get_attribute('innerHTML')
    print(email)
    return email

def solver(problem):
    problem = str(problem)
    problem = problem.replace(" ", "")
    problem = problem.replace("=", "")
    f, l = problem.split("+")
    f = int(f)
    l = int(l)
    return f + l


if __name__ == '__main__':
    main()
