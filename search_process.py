# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 11:09:36 2022

@author: Januario Cipriano
"""

import re
import os
import time
import json
import logging
import numpy as np
import pandas as pd
from glob import glob
from enum import Enum
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# local modules
from instantiate_driver import initiate_driver
from classify_proposal import ClassifyProposal
    
def launch_driver():
    URL = 'http://10.245.87.77/itcore.sites/ITCore.Ui.Web/ITCore.aspx'
    driver = initiate_driver()
    driver.get(URL)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

# driver = launch_driver()

def get_row(path_id):
    client_data = {}
    common_idenifier = '//*[@id="ContentPlaceHolder1_flwForm_egvSearchResult'
    identifiers = ['lbResultProcessNumber', 'lbResultTipo', 'lbResultClientName', 'lbResultUser', 
                   'lbResultCurrentCostCenter', 'lbResultCurrentUser', 'lbResultCreationDate',
                   'lbResultStatus']
    for identifier in identifiers:
        path = f'{common_idenifier}_{identifier}_{path_id}"]'
        path = driver.find_element(By.XPATH, path)
        col_name = identifier.split('lbResult')[1]
        client_data[col_name] = path.text
        
    client_no = driver.find_element(By.XPATH, f'{common_idenifier}"]/tbody/tr[2]/td[4]')
    client_data['client_no'] = client_no.text
    
    print(client_data)
    return client_data


def search_client_process(driver):
    classify = ClassifyProposal()
    
    process_numbers = classify.get_process_numbers()
    number_of_iterations = len(process_numbers)
    print(f'PROCESS NUMBERS = {process_numbers}')
    
    for i in range(number_of_iterations):
        # start_time = datetime.now()
        process_number = process_numbers[i]   # 1154192
        print(f'CURRENT PROCESS NUMBER = {process_number}')
        logging.warning(f'Handling PROCESS NUMBER {process_number}')


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
                    
                    classify.set_search_results(process_number, required_values)
                except Exception as err:
                    print("==== ERROR ATTEMPTING TO CHANGE FRAME ====")
                    print(err)
                    
            except Exception as e:
                print(e)
            
            time.sleep(0.5)
            driver.refresh()
            time.sleep(0.5)
            
        except Exception as e:
            print(e)


def main():
    # driver = launch_driver()
    search_client_process()

# if __name__=='__main__':
#     main()
#     count = 3
#     driver = launch_driver()
#     while count > 0:
#         main()
#         count -= 1




".\A200795"












