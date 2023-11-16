import re
import json
import time
import logging
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from data_structure import Process
from access_page import fetch_table_page
from instantiate_driver import initiate_driver
# from search_process2 import search_client_process

adt = Process()

# if __name__=='__main__':
# 	fetch_table_page(3)

".\A200795"

URL = 'http://10.245.87.77/itcore.sites/ITCore.Ui.Web/ITCore.aspx'

driver = initiate_driver()

driver.get(URL)

WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

dept_processes = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_BtnDepartmentWorklist"]')
dept_processes.click()
time.sleep(10)

".\A200795"


def refrech_page():
	driver.refresh()
	time.sleep(7)
	# WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
	# driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

class Classify(Enum):
    FIRST = 'NWOW'
    SECOND = 'CVU Central'


def search_client_process(df, process_numbers):
    number_of_iterations = len(process_numbers)
    print(f'PROCESS NUMBERS = {process_numbers}')
    
    time_tracker = []
    for i in range(number_of_iterations):
        start_time = datetime.now()
        process_number = process_numbers[i]   # 1154192
        print(f'CURRENT PROCESS NUMBER = {process_number}')
        logging.warning(f'Handling PROCESS NUMBER {process_number}')

        # if check_if_is_updated(df, process_number):

        print(f'================== ITERATION {i} ==================')
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_LkCustMenu_3"]/div')))
        
        menu = driver.find_element(By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_LkCustMenu_3"]/div')
        hidden_submenu = driver.find_element(By.XPATH, '//*[@id="contentContainer_TMenus_rpCustMenu_rpSubCustMenu_3_rpSubCustMenuChilds_0_LkSubMenuChild_0"]')
        actions = ActionChains(driver)
        actions.move_to_element(menu)
        actions.click(hidden_submenu)
        actions.perform()
        time.sleep(1.5)
        logging.warning('Successfully clicked on search href.')

        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
        driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

        try:
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_ntbcProcessNumber_txField"]')))
            search_process_field_XPATH = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_ntbcProcessNumber_txField"]')
            search_process_field_XPATH.send_keys(str(process_number))
            time.sleep(0.5)
            logging.warning('Successfully inserted PROCESS NUMBER into input field')
            
            search_button_XPATH = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fcontrols_btnSearch"]/span[2]')
            search_button_XPATH.click()
            logging.warning('Successfully clicked on Search button')
            # time.sleep(30)

            try:
                WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_egvSearchResult"]/tbody/tr[2]')))
                client_td = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_egvSearchResult"]/tbody/tr[2]')
                client_td.click()
                time.sleep(1.5)
                logging.warning(f'Successfully clicked on CLIENT result')
                
                WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ui-id-2"]/span')))
                financial_deails = driver.find_element(By.XPATH, '//*[@id="ui-id-2"]/span')
                financial_deails.click()
                time.sleep(0.2)
                
                requested_amount = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_tabs_fic1b_txt_GoodValue"]')
                requested_amount = re.findall(r'\d+', requested_amount.text)
                requested_amount = float(''.join(requested_amount[:-1]) + '.'+ requested_amount[-1])
                required_values = {
                    'Valor_Requisitado': requested_amount   
                }
                
                time.sleep(0.2)
                proponents = driver.find_element(By.XPATH, '//*[@id="st_2"]/span[1]')
                proponents.click()
                time.sleep(0.2)
                
                verificar_proponents = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ff1_fc1_finTit_dgInterveners_ctl02_btnDetailIntervener"]')
                verificar_proponents.click()
                time.sleep(0.2)
                # print('==== SHOWING POPUP ====')
                
                driver.switch_to.parent_frame()
                time.sleep(0.2)
                # print("==== SWITCHED BACK TO PARENT FRAME ====")
                
                try:
                    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'PopupMainIframeShowAddIntervener_Popup')))
                    driver.switch_to.frame(driver.find_element(By.ID, 'PopupMainIframeShowAddIntervener_Popup'))
                    # print("==== SWITCHED FRAME ====")
                    
                    profissao_entidade_patronal = driver.find_element(By.XPATH, '//*[@id="ui-id-5"]/span')
                    profissao_entidade_patronal.click()
                    time.sleep(0.2)
                    
                    entidade_patronal = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_PopupContainer_detalhePropop_tabs_fic4c_txtProfessionalEmployer"]')
                    entidade_patronal = entidade_patronal.text
                    required_values['Entidade-Patronal'] = entidade_patronal
                    print(json.dumps(required_values, indent=4))
                    logging.warning(f'Data extracted successfully for PROCESS NUMBER {process_number}')
                    
                    # update_excel_file(df, process_number, required_values)
                    # classify.set_search_results(process_number, required_values)

                    df[df['process_number'] == process_number]['ValorRequisitado'] = requested_amount
                    df[df['process_number'] == process_number]['Colaborador2'] = entidade_patronal
                    df[df['process_number'] == processos]['Entidade-Patronal'] = entidade_patronal

                    if df.loc[process_number, 'Valor Requisitado'] > 500000:
                    	df.loc[process_number, 'Area de Verificacao'] = Classify.SECOND.value
                    elif df.loc[process_number, 'Valor Requisitado'] == 0:
                    	pass
                    elif df.loc[process_number, 'Valor Requisitado'] <= 500000:
                    	df.loc[process_number, 'Area de Verificacao'] = Classify.FIRST.value

                except Exception as err:
                    print("==== ERROR ATTEMPTING TO CHANGE FRAME ====")
                    print(err)
                    
            except Exception as e:
                print(e)
            
            time.sleep(0.5)
            driver.refresh()
            time.sleep(0.5)
            
            end_time = datetime.now()
            time_tracker.append([start_time, end_time])
        except Exception as e:
            print(e)

    print(time_tracker)
    try:
        df_time_tracer = pd.read_csv('time-tracer.xlsx')
    except Exception as e:
        df_time_tracer = None

    time_tracker = pd.DataFrame(time_tracker, columns=['start-time', 'end-time'])
    time_tracker['start-time'] = pd.to_datetime(time_tracker['start-time'])
    time_tracker['end-time'] = pd.to_datetime(time_tracker['end-time'])
    time_tracker['time-diff'] = time_tracker['end-time'] - time_tracker['start-time']
    print(time_tracker)

    refrech_page()



def fetch_process_number():
	for path_id in range(0, 15):
		process_path = f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_gridAbertConta_lb_nProcesso_{path_id}"]'
		try:
			process_tag = driver.find_element(By.XPATH, process_path)
			print(process_tag.text)
			adt.add(process_tag.text)
		except Exception as e:
			pass
			# print(e)


def fetch_remaining_pages():
	link_ids = []
	for link_id in range(1, 30):
		try:
			link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{link_id}"]')
			link_ids.append(link_id)
		except Exception as e:
			pass
			# print(e)
			# logging.warning(exc)

	for link_id in link_ids:
		print(f'\nFETCHING PAGE = {link_id}')
		try:
			link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{link_id}"]')
			link.click()
			time.sleep(10)
			fetch_process_number()
			time.sleep(4)
		except Exception as exc:
			pass
			# print(exc)
			# logging.warning(exc)
		print(f'FINISHED FETCHING PAGE = {link_id}')



def main():
	fetch_process_number()
	time.sleep(2)

	# fetch_remaining_pages()

	df = adt.create_dataframe()
	# df = pd.read_excel('./Classified Proposals/Processos.xlsx')
	# process_numbers = df['process_number'].values.tolist()

	# refrech_page()
	# driver.switch_to.parent_frame()
	# driver.refresh()
	# time.sleep(7)
	# WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
	# driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

	# search_client_process(process_numbers)


if __name__=='__main__':
	main()


".\A200795"



