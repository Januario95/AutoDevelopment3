import json
import time
import logging
import pandas as pd
from glob import glob
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from instantiate_driver import initiate_driver
from data_structure import ADT, NodeStructure


adt = ADT()

def get_row(driver, path_id):
	# print(f'FETCHING ROW: {path_id}')
	row_data = {}
	common_idenifier = '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_gridAbertConta'
	identifiers = ['lb_timer', 'lb_nProcesso', 'lb_tipoConta', 'lb_nome', 'span_Segmento',
	               'lb_estado', 'lb_branch', 'lb_user']
	    
	for identifier in identifiers:
	    path = f'{common_idenifier}_{identifier}_{path_id}"]'
	    path = driver.find_element(By.XPATH, path)
	    col_name = identifier.split('_')[1]
	    row_data[col_name] = path.text

	R = driver.find_element(By.XPATH, f'{common_idenifier}"]/tbody/tr[{2+path_id}]/td[7]')
	row_data['R'] = R.text

	creation_date = driver.find_element(By.XPATH, f'{common_idenifier}"]/tbody/tr[{2+path_id}]/td[8]')
	row_data['CreationDate'] = creation_date.text
	row_data['ModificadoEm'] = datetime.now()
	row_data['ValorRequisitado'] = 0
	row_data['Colaborador2'] = 'CVU Central'
	row_data['EntidadePatronal'] = 'Nao Definida'
	row_data['IsUpdated'] = False
	    
	node = NodeStructure(**row_data)
	# print(node.values)
	adt.push(node)


def fetch_remaining_rows(driver): # , new_refetch_rows):
	files = glob('*.xlsx')
	df = pd.read_excel(files[0])

	# URL = 'http://10.245.87.77/itcore.sites/ITCore.Ui.Web/ITCore.aspx'
	# driver = initiate_driver()
	# driver.get(URL)

	# WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "MainIframe")))
	# driver.switch_to.frame(driver.find_element(By.ID, "MainIframe"))

	# dept_processes = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_BtnDepartmentWorklist"]')
	# dept_processes.click()
	# time.sleep(10)

	process_numbers = {}
	for page_id in range(30):
		try:
			print(f'PAGE ID = {page_id}')
			link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{page_id}"]')
			link.click()
			time.sleep(7)

			common_idenifier = '//*[@id="ContentPlaceHolder1_flwForm_fwcInit_gridAbertConta'
			identifier = 'lb_nProcesso'
			    
			process_numbers_ = []
			for td_num in range(0, 15):
				try:
				    path = f'{common_idenifier}_{identifier}_{td_num}"]'
				    path = driver.find_element(By.XPATH, path)

				    if df[df['Nº'] == int(path.text)].shape[0] == 0:
				    	process_numbers_.append(td_num)
				except Exception:
					pass

				time.sleep(1)
			# print(process_numbers_)
			process_numbers[page_id] = process_numbers_
		except Exception:
			pass

	# df = pd.DataFrame(process_numbers)
	time.sleep(2)
	print(process_numbers)

	for key, arr in process_numbers.items():
		table_page = key

		try:
			link = driver.find_element(By.XPATH, f'//*[@id="ContentPlaceHolder1_flwForm_fwcInit_grvPager_repPager_pb1_{table_page}"]')
			link.click()
			time.sleep(8)

			for path_id in arr:
				get_row(driver, key)
				print(f"ROW = {path_id} in PAGE = {table_page}")
				time.sleep(1.5)
		except Exception as e:
			pass
	print('FINISHED RE-FECHING ROWS==========================')


def save_df_and_merge():
	files = glob('*.xlsx')
	df1 = pd.DataFrame(adt.data)
	print(df1.columns)
	if df1.shape[0] > 0:
		df1.columns = 'SLA, Nº, Tipo, Nome, Segmento, Estado, Balcão de Criação, Colaborador, R, Dt. Criação, DownloadedAt, Valor Requisitado, Area de Verificacao, Entidade Patronal, IsUpdated'.split(', ')
		df2 = pd.read_excel(files[0])
		df3 = df1.append(df2)
		print(df1.shape)
		print(df2.shape)
		print(df3.shape)
		df3.set_index('Nº', )
		df3.drop_duplicates('Nº', inplace=True)
		df3.to_excel(files[0], index=False)
	else:
		print('UNABLE TO SAVE TO FILE=============')

	print('FINISHED SAVING FILES=====================')


	

# if __name__=='__main__':

# 	fetch_remaining_rows() # new_refetch_rows)

# 	save_df_and_merge()


"A169810"









































