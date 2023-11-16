from instantiate_driver import initiate_driver

URL = 'http://10.245.87.77/itcore.sites/ITCore.Ui.Web/ITCore.aspx'

driver = initiate_driver()

driver.get(URL)

WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

dept_processes = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_BtnDepartmentWorklist"]')
dept_processes.click()
time.sleep(10)

print('Starting...')

adt = ADT()

