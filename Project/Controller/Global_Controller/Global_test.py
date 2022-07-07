from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .Global_xpath import LoginXpath
from flask import flash
from .Global_xpath import CalendarDateRangeXpath
import time
from selenium.webdriver.common.keys import Keys

class Login:
    @staticmethod
    def login(driver, url, username, password):
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities=d)
        # driver.implicitly_wait(30)

        res = Login.openUrl(driver, url)

        if not res["success"]:
            flash(res["message"], category="error")
            driver.quit()
            return False


        username_xpath = LoginXpath.username
        password_xpath = LoginXpath.password
        loginbtn_xpath = LoginXpath.login_btn

        # landing page
        
        res = Login.authenticate(driver, username_xpath, password_xpath, loginbtn_xpath, username, password)
        
        if not res['success']:
            flash(res["message"], category="error")
            driver.quit()
            return False

        return driver

    @staticmethod
    def authenticate(driver, username_xpath, password_xpath, loginbtn_xpath, username, passwd):
        # email = WebDriverWait(driver, 120).until(
        #     EC.presence_of_element_located((By.XPATH, f"{username}"))
        # )
        email = driver.find_element(by=By.XPATH, value=f'{username_xpath}')
        email.send_keys(username)
        password = driver.find_element(by=By.XPATH, value=f'{password_xpath}')
        password.send_keys(passwd)
        loginbtn = driver.find_element(by=By.XPATH, value=f'{loginbtn_xpath}')

        loginbtn.click()

        try:
            # element = WebDriverWait(driver, 120).until(
            #     EC.presence_of_element_located((By.XPATH, LoginXpath.login_error))
            # )
            element = WebDriverWait(driver, 120).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, LoginXpath.login_error)), 
                    EC.presence_of_element_located((By.XPATH, LoginXpath.main_header))
                )
            )
            # element = driver.find_element(
            #     by = By.XPATH,
            #     value = LoginXpath.main_header
            # )
            # print(f"{element} {element.text}")
            print("Login success")

            if "These credentials do not match our records" in element.text:
                return {
                    "success": False,
                    "message": "Invalid credentials."
                }
            
        except Exception as e:
            print(e)
        return{
            "success": True
        }

    @staticmethod
    def openUrl(driver, url):
        driver.get(url)
        
        try:
            # element = WebDriverWait(driver, 120).until(
            #     EC.presence_of_element_located((By.XPATH, LoginXpath.no_vpn))
            # )

            element = driver.find_element(
                by = By.XPATH,
                value = LoginXpath.no_vpn
            ).text
            if "Network Error" in element:
                
                return {
                    "success": False,
                    "message": "Not connected to the Jarvis Network."
                }
            else:
                print("Connected to Jarvis Network")
        except Exception as e:
            pass

        try:
            # element = WebDriverWait(driver, 120).until(
            #     EC.presence_of_element_located((By.XPATH, LoginXpath.logo_xpath))
            # )
            element = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, LoginXpath.logo_xpath))
            )
            # element = driver.find_element(
            #     by = By.XPATH,
            #     value = LoginXpath.logo_xpath
            # )
            print(f"Valid URL {element}")
        except Exception as e:
            print("Invalid Url")
            return {
                "success": False,
                "message": "Invalid Jarvis Analytics URL."
            }

        return {
            "success": True
        }


# Calendar Date Range
month_list = {"01": "1", "02": "2", "03": "3", "04": "4", "05": "5", "06": "6",
              "07": "7", "08": "8", "09": "9", "10": "10", "11": "11", "12": "12"}

def calendarDateRange(driver, date_from, date_to):
    yf, mf, df = date_from.split('-')

    yt, mt, dt = date_to.split('-')
    time.sleep(5)
    dateElement = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.date_picker}")))
    dateElement.click()

    if yf == yt and mf == mt:
        # Select Month
        month_option = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_monthfrom}"))
        )
        month_option.click()

        month = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH,
                                              f"/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/thead/tr/th[2]/div/select/option[{month_list[mf]}]"))
        )
        month.click()

        # Input Year
        clear_year = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearfrom}"))
        )
        clear_year.send_keys(Keys.CONTROL + "a")

        clear_year = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearfrom}"))
        )
        clear_year.send_keys(Keys.DELETE)

        year = WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearfrom}"))
        )
        year.send_keys(yf)

        # Date clicked
        fromDate = driver.find_element(by=By.XPATH,
                                       value=f'//html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr/td[ text() = {df} and (@class="" or @class="weekend" or @class="in-range"  or @class="today active in-range end-date" or @class="weekend in-range" or @class="active in-range start-date" or @class="weekend today active in-range end-date" or @class="active in-range end-date" or @class="weekend today in-range" or @class="weekend today")]')
        fromDate.click()

        toDate = driver.find_element(by=By.XPATH,
                                     value=f'//html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr/td[ text() = {dt} and (@class="" or @class="weekend" or @class="in-range"  or @class="today active in-range end-date" or @class="weekend in-range" or @class="active in-range start-date" or @class="weekend today active in-range end-date" or @class="active in-range end-date" or @class="weekend today in-range" or @class="weekend today")]')
        toDate.click()

    else:
        dateFrom(driver, yf, mf, df)
        dateTo(driver, yt, mt, dt)

def dateFrom(driver, yf, mf, df):
    # Select Month
    month_option = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_monthfrom}"))
    )
    month_option.click()

    month = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH,
                                          f"/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/thead/tr/th[2]/div/select/option[{month_list[mf]}]"))
    )
    month.click()

    # Input Year
    clear_year = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearfrom}"))
    )
    clear_year.send_keys(Keys.CONTROL + "a")

    clear_year = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearfrom}"))
    )
    clear_year.send_keys(Keys.DELETE)

    year = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearfrom}"))
    )
    year.send_keys(yf)

    # Date clicked
    fromDate = driver.find_element(by=By.XPATH,
                                   value=f'//html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/table/tbody/tr/td[ text() = {df} and (@class="" or @class="weekend" or @class="in-range"  or @class="today active in-range end-date" or @class="weekend in-range" or @class="active in-range start-date" or @class="weekend today active in-range end-date" or @class="active in-range end-date" or @class="weekend today in-range" or @class="weekend today")]')
    fromDate.click()

def dateTo(driver, yt, mt, dt):
    # Select Month
    month_option = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_monthto}"))
    )
    month_option.click()

    month = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH,
                                          f"/html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/thead/tr/th[2]/div/select/option[{mt}]"))
    )
    month.click()

    # Input Year
    clear_year = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearto}"))
    )
    clear_year.send_keys(Keys.CONTROL + "a")

    clear_year = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearto}"))
    )
    clear_year.send_keys(Keys.DELETE)

    year = WebDriverWait(driver, 120).until(
        EC.visibility_of_element_located((By.XPATH, f"{CalendarDateRangeXpath.curr_yearto}"))
    )
    year.send_keys(yt)

    # Date clicked
    toDate = driver.find_element(by=By.XPATH,
                                   value=f'//html/body/div[1]/main/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr/td[ text() = {dt} and (@class="" or @class="weekend" or @class="in-range"  or @class="today active in-range end-date" or @class="weekend in-range" or @class="active in-range start-date" or @class="weekend today active in-range end-date" or @class="active in-range end-date" or @class="weekend today in-range" or @class="weekend today")]')
    toDate.click()
