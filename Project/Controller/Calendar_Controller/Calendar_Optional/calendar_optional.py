from selenium import webdriver
from selenium.webdriver.common.by import By
from flask_login import login_required, current_user
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from datetime import datetime
from ....models import CalendarFilterUse
from ....models import CalendarFilterTesting
from .... import db
import sqlite3
import re


def providerFilterTest(driver, test_code):
    driver.implicitly_wait(1000000000)
    new_provider = CalendarFilterUse(user_id = current_user.id,
        test_code = test_code,
        filter_name = "Provider Filter",
        created_at = datetime.now(),
        updated_at = datetime.now())
    
    db.session.add(new_provider)
    db.session.commit()

    getProvider = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Provider Filter').order_by(CalendarFilterUse.id.desc()).first()

    stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/span/span/span").text

    clickProviderFilterButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/button")
    clickProviderFilterButton.click()

    clickAllProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/div/div[2]/div[1]/div/button[1]")
    clickAllProvider.click()

    getNumberOfProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/div/div[2]/div[1]/span/span").text.replace('(', '').replace(')', '')
    # countProvider = re.split('(|)', getNumberOfProvider)

    for x in range(int(getNumberOfProvider)):
        driver.implicitly_wait(1000000000)
        totalPass = 0
        totalFail = 0

        clickClearProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/div/div[2]/div[1]/div/button[2]")
        clickClearProvider.click()
        
        getProviderText = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/div/div[2]/ul/li["+str(x+1)+"]/span/span[2]").text

        selectProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/div/div[2]/ul/li["+str(x+1)+"]/span/span[2]")
        selectProvider.click()

        clickApplyButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/div/div[3]/button[2]")
        clickApplyButton.click()

        stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/span/span/span").text

        getText = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/span").text
        splitNumberOfItems = getText.split("-")
        countData = splitNumberOfItems[-1]

        pts_name_pass = ''
        proc_code_pass = ''
        pts_name_fail = ''
        proc_code_fail = ''
        unsearch_provider = ''
        for y in range(int(countData)):  
            getProviderTextTable = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr["+str(y+1)+"]/td[13]/span/span[1]/span").text
            
            if getProviderText == getProviderTextTable:
                pts_name_pass = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr["+str(y+1)+"]/td[2]/span/span[1]/span").text
                proc_code_pass = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr["+str(y+1)+"]/td[14]").text
                totalPass = totalPass + 1
            else:
                pts_name_fail = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr["+str(y+1)+"]/td[2]/span/span[1]/span").text
                proc_code_fail = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr["+str(y+1)+"]/td[14]").text
                unsearch_provider = driver.finde_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr["+str(y+1)+"]/td[13]/span/span[1]/span").text
                totalFail = totalFail + 1
        stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/span/span/span").text

        if totalFail == 0:
            new_calendar_testing = CalendarFilterTesting(user_id = current_user.id,
                test_code = test_code,
                filter_id = getProvider.id,
                search_provider = getProviderText,
                patient_name = pts_name_pass,
                procedure_code = proc_code_pass,
                unsearch_provider = 'None',
                status = 'Pass',
                created_at = datetime.now(),
                updated_at = datetime.now())

            db.session.add(new_calendar_testing)
            db.session.commit()
        else:
            new_calendar_testing = CalendarFilterTesting(user_id = current_user.id,
                test_code = test_code,
                filter_id = getProvider.id,
                search_provider = getProviderText,
                patient_name = pts_name_fail,
                procedure_code = proc_code_fail,
                unsearch_provider = unsearch_provider,
                status = 'Fail',
                created_at = datetime.now(),
                updated_at = datetime.now())
            
            db.session.add(new_calendar_testing)
            db.session.commit()


        clickProviderFilterButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/button")
        clickProviderFilterButton.click()
        

    
    return driver

def procedureFilterTest(driver, test_code):
    driver.implicitly_wait(1000000000)
    # new_provider = CalendarFilterUse(user_id = current_user.id,
    #     test_code = test_code,
    #     filter_name = "Provider Filter",
    #     created_at = datetime.now(),
    #     updated_at = datetime.now())
    
    # db.session.add(new_provider)
    # db.session.commit()

    # getProvider = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Provider Filter').order_by(CalendarFilterUse.id.desc()).first()

    stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/span/span/span").text

    clickProcedureFilterButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/button")
    clickProcedureFilterButton.click()

    getColumnInProcFilter = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[2]/div/div/div[2]/ul/li")
    count = len(getColumnInProcFilter)

    print(count)

    # getNumberOfProvider = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[1]/div/div/div[2]/div[1]/span/span").text.replace('(', '').replace(')', '')
    return driver

def patientFilterTest(driver, test_code):
    driver.implicitly_wait(1000000000)
    # new_provider = CalendarFilterUse(user_id = current_user.id,
    #     test_code = test_code,
    #     filter_name = "Provider Filter",
    #     created_at = datetime.now(),
    #     updated_at = datetime.now())
    
    # db.session.add(new_provider)
    # db.session.commit()

    # getProvider = CalendarFilterUse.query.filter_by(test_code=test_code).filter_by(filter_name='Provider Filter').order_by(CalendarFilterUse.id.desc()).first()

    stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/span/span/span").text

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/button'))) 
    
    getAllDataInsideTbody = driver.find_elements(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr")
    checkIfTheresData = len(getAllDataInsideTbody)

    if checkIfTheresData != 0:
        getText = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/span").text
        splitNumberOfItems = getText.split("-")
        countData = splitNumberOfItems[-1]  


        

        if int(countData) > 10:
            arrayOfPatientToTest = []
            for x in range(10):
                getPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr["+str(x+1)+"]/td[2]/span/span[1]/span").text
                splittingPatientName = getPatient.split(' ')
                rearrangePatientName = splittingPatientName[-1]+", "+splittingPatientName[-2]
                arrayOfPatientToTest.append(rearrangePatientName)
            
            countPatient = len(arrayOfPatientToTest)
            for y in range(countPatient):
                clickPatientFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/button")
                clickPatientFilter.click()

                searchPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/div/div[1]/input").clear()

                searchPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/div/div[1]/input")
                searchPatient.send_keys(arrayOfPatientToTest[y])

                clickPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/div/div[2]/ul/li")
                clickPatient.click()

                clickApplyButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/div/div[3]/button[2]")
                clickApplyButton.click()

                stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/span/span/span").text

                getText = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/span").text
                splitNumberOfItems = getText.split("-")
                countDatas = splitNumberOfItems[-1]

                pts_name_pass = ''
                proc_code_pass = ''
                pts_name_fail = ''
                proc_code_fail = ''
                unsearch_provider = ''


                # LOOP HERE
                
                clickPatientFilter = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/button")
                clickPatientFilter.click()

                unclickPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/div/div[2]/ul/li")
                unclickPatient.click()

                searchPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/div/div[1]/input").clear()

                clickApplyButton = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[1]/div/div[3]/div/div/div[3]/button[2]")
                clickApplyButton.click()

                stopperGetLoc = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/span/span/span").text

                print(countDatas)
                
        if int(countData) < 10:
            for x in range(int(countData)):
                getPatient = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/span/div[2]/div/div[2]/div/div[1]/table/tbody/tr["+str(x+1)+"]/td[2]/span/span[1]/span").text
                splittingPatientName = getPatient.split(' ')
                rearrangePatientName = splittingPatientName[-1]+", "+splittingPatientName[-2]
                arrayOfPatientToTest.append(rearrangePatientName)

            countPatient = len(arrayOfPatientToTest)
            for y in range(countPatient):
                print("HELLO")


    
    return driver
