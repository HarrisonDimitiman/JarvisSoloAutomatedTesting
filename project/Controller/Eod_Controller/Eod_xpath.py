from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Element:
    def __init__(self, name, xpath, type):
        self.element = None
        self.name = name
        self.xpath = xpath
        self.type = type
        self.instantiated = False

    def instantiateElement(self, driver):
        self.instantiated = True
        try:
            self.element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, self.xpath))
            )
        except: 
            pass
    
    def getElement(self):
        return self.element

# InputElement, CollectionElement, and TextElement implements different getValue().
# Message to future eyd: Need to find way to require the implementation of the getValue method of children classes inherting the Element class.

class InputElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "value")
    
    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return self.element.get_attribute('value')

class TextElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "value")
    
    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return self.element.text

class CollectionElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "collection")

    def getValue(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")

        return len(self.element)

class ClickableElement(Element):
    def __init__(self, name, xpath):
        super().__init__(name, xpath, "button")

    def click(self):
        if self.element == None: 
            raise Exception("Element not instantiated.")
        
        self.element.click()

# BEYOND ARE HARDCODED XPATHS, NEED TO CHANGE IMPLEMENTATION LATER TO INCOPORATE DATABASE CALLS

class EodXpath:
    collection = InputElement('collection','/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[13]/div[2]/input')
    adjustments = InputElement('adjustments', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[12]/div[2]/input')
    case_acceptance = InputElement('case_acceptance','/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[20]/div[2]/input')
    missing_ref = InputElement('missing_ref', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[24]/div[2]/input')
    no_show = InputElement('no_show', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[17]/div[2]/input')
    daily_coll = InputElement('daily_coll', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[14]/div[2]/input')
    hyg_reapp = InputElement('hyg_reapp', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[28]/div[2]/input')
    new_patients = InputElement('new_patients', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[21]/div[2]/input')
    same_day_treat = InputElement('same_day_treat', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[18]/div[2]/input')
    pt_portion = InputElement('pt_portion', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[5]/div[2]/input')

class BreakdownXpath:
    collection = ClickableElement('collection', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[13]/div[1]/div/span/a')
    adjustments = ClickableElement('adjustments', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[12]/div[1]/div/span/a')
    case_acceptance = ClickableElement('case_acceptance', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[20]/div[1]/label/span/a')
    missing_ref = ClickableElement('missing_ref', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[24]/div[1]/label/div/a')
    no_show = ClickableElement('no_show', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[17]/div[1]/label/div/a')
    daily_coll = ClickableElement('daily_coll', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[14]/div[1]/label/div/a')
    hyg_reapp = ClickableElement('hyg_reapp', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[28]/div[1]/label/div/a')
    new_patients = ClickableElement('new_patients', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[2]/div[12]/div[1]/label/div/a')
    same_day_treat = ClickableElement('same_day_treat', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[18]/div[1]/label/div/a')
    pt_portion = ClickableElement('pt_portion', '/html/body/div[1]/main/div[2]/div[3]/div[1]/div/form/div/div[1]/div[1]/div/div[5]/div[1]/label/div/a')

# june 21 and some other dates for missing ref and new patients
class ModalMetricXpath:
    collection = TextElement('collection', '/html/body/div[1]/main/div[3]/div[9]/div/div/div[3]/div[1]/div/table/tfoot/tr/td[6]')
    adjustments = TextElement('adjustments', '/html/body/div[1]/main/div[3]/div[2]/div/div/div[3]/div[1]/div/table/tfoot/tr/td[6]')
    case_acceptance = TextElement('case_acceptance', '/html/body/div[1]/main/div[3]/div[9]/div/div/div[2]/div[1]/div/table/tfoot/tr[1]/td[6]')
    # missing ref is number of rows
    missing_ref = CollectionElement('missing_ref', '/html/body/div[1]/main/div[3]/div[7]/div/div/div[2]/div[2]/div/table/tbody/tr')
    no_show = TextElement('no_show', '/html/body/div[1]/main/div[3]/div[4]/div/div/div[2]/div[2]/div/table/tr/td[2]/strong/span')
    daily_coll = TextElement('daily_coll', '/html/body/div[1]/main/div[3]/div[3]/div/div/div[2]/div[2]/div/table/tr/td[4]/strong/span')
    hyg_reapp = TextElement('hyg_reapp', '/html/body/div[1]/main/div[3]/div[8]/div/div/div[2]/div[2]/div/table/tr/td[3]/strong/span')
    # new patients is number of rows
    new_patients = CollectionElement('new_patients', '/html/body/div[1]/main/div[3]/div[6]/div/div/div[2]/table/tbody/tr')
    same_day_treat = TextElement('same_day_treat', '/html/body/div[1]/main/div[3]/div[5]/div/div/div[2]/div[2]/div/table/tr[2]/td[5]/strong/span')
    pt_portion = TextElement('pt_portion', '/html/body/div[1]/main/div[3]/div[1]/div/div/div[2]/div[2]/div/table/tr[1]/td[2]/strong/span')

class EodSetupXpath:
    date_picker = '//*[@class="vue-daterange-picker w-full"]'
    location_picker = '/html/body/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]'
    refresh_btn = '/html/body/div[1]/main/div[1]/div/div/div/div[3]/button'

