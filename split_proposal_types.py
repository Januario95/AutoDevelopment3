import os
import json
import time
import numpy as np
import pandas as pd
from glob import glob
import win32com.client
from datetime import datetime



def send_email(receiver, subject, body, attachment):
	engine = win32com.client.Dispatch('outlook.application')
	email = engine.CreateItem(0)
	email.Recipients.Add(receiver)
	email.Subject = subject
	email.HtmlBody = f'<h4 style="text-align:center;font-style:italic;">{body}</h4>'
	email.attachments.Add(attachment)
	email.send

def get_dataframe_and_send(df, type_):
	d = df[df['Area de Verificacao'] == type_]
	now = datetime.now()
	if now.hour < 12:
		now = now.date().strftime('%d.%m.%Y')
		filename = type_.upper() # replace(' ', '_').lower()
		filename = f'{filename} - {now} (Manha).xlsx'
	else:
		now = now.date().strftime('%d.%m.%Y')
		filename = type_.title() # replace(' ', '_').lower()
		filename = f'{filename} - {now} (Tarde).xlsx'
	filename = f'C:/Users/a248433/Documents/SB Mozambique/EDO/Robotics/Bots/Automatizacao do processo de extracao do fluxo/Classified Proposals/{filename}.xlsx'
	d.to_excel(filename, index=False)
	time.sleep(2)

	# styler = d.style.applymap(highlight_sla, subset=['SLA'])
	# styler.to_excel(filename, index=False)

	# print(os.path.exists(filename))

	if type_ == 'NWOW':
		send_email(receiver='januario.cipriano@standardbank.co.mz', 
				   subject='New Ways Of Work',
				   body='This email is for NWOW', 
				   attachment=filename)
		print('Email sent for NWOW proposals')
	if type_ == 'CVU Central':
		send_email(receiver='januario.cipriano@standardbank.co.mz', 
				   subject='CVU Central',
				   body='This email is for CVU Central', 
				   attachment=filename)
		print('Email sent for CVU Central proposals')

	# os.remove(filename)
	# print(f"{filename.split('/')[-1]} successfully removed!")


def get_dataframe_then_send(emails, type_):
	# emails = ['mozverification@mail.standardbank.com', 
	# 		  'gerentesregionais@mail.standardbank.com']

	for email in emails:
		# filename = 'NWOW' if type_ == 'NWOW' else 'cvu_central'
		if type_ == 'NWOW':
			filename = f'C:/Users/a248433/Documents/SB Mozambique/EDO/Robotics/Bots/Automatizacao do processo de extracao do fluxo/Classified Proposals/Fluxo_nwow.xlsx'
			send_email(receiver=email, 
					   subject='New Ways Of Work',
					   body='This email is for NWOW', 
					   attachment=filename)
		elif type_ == 'CVU Central':
			filename = f'C:/Users/a248433/Documents/SB Mozambique/EDO/Robotics/Bots/Automatizacao do processo de extracao do fluxo/Classified Proposals/Fluxo_cvu_central.xlsx'
			send_email(receiver='januario.cipriano@standardbank.co.mz', 
				       subject='CVU Central',
				       body='This email is for CVU Central', 
				       attachment=filename)


def set_color(row):
    if row == 'NWOW':
        return 'background-color: red'
    elif row == 'CVU Central':
        return 'background-color: teal'

def highlight_sla(val):
    return 'color: red;'


def split_proposal():
	files = glob('*.xlsx')

	df = pd.read_excel(files[0])
	del df['IsPropostaActualizada']
	for col in ['DownloadedAt', 'IsUpdated', 'ModificadoEm']:
		try:
			del df[col]
		except:
			pass

	def modify_column(val):
		if val == 'Nao Definida':
			return ''
		return val

	def modify_column2(val):
		if val == 0:
			return ''
		return val
	
	df['Entidade Patronal'] = df['Entidade Patronal'].apply(modify_column)
	df['Valor Requisitado'] = df['Valor Requisitado'].apply(modify_column2)
	df.replace(np.nan, '', inplace=True)
	staff = df[df['Segmento'].str.contains('Staff')]
	del staff['Entidade Patronal']
	df = df[df['Segmento'] != 'Staff']

	# df.to_excel(f'C:/Users/a248433/Documents/SB Mozambique/EDO/Robotics/Bots/Automatizacao do processo de extracao do fluxo/Classified Proposals/general.xlsx', index=False)

	now = datetime.now()
	if now.hour < 12:
		now = now.date().strftime('%d.%m.%Y')
		filename = f'Staff - {now} (Manha).xlsx'
	else:
		now = now.date().strftime('%d.%m.%Y')
		filename = f'Staff - {now} (Tarde).xlsx'
	filename = f'C:/Users/a248433/Documents/SB Mozambique/EDO/Robotics/Bots/Automatizacao do processo de extracao do fluxo/Classified Proposals/{filename}'
	staff.to_excel(filename, index=False)
	df = df[df['Segmento'] != 'Staff']

	get_dataframe_and_send(df, 'CVU Central')
	get_dataframe_and_send(df, 'NWOW')

	# send_email(receiver='januario.cipriano@standardbank.co.mz', 
	# 		   subject='Segmento Staff',
	# 		   body='This email is for Segmento Staff', 
	# 		   attachment=filename)


	# cvu_central_nwow = ['mozverification@mail.standardbank.com', 
	# 					'gerentesregionais@mail.standardbank.com']
	# get_dataframe_then_send(df, cvu_central_nwow)

	# for email in cvu_central_nwow:
	# 	all_ = df.copy(deep=True)
	# 	filename = f'C:/Users/a248433/Documents/SB Mozambique/EDO/Robotics/Bots/Automatizacao do processo de extracao do fluxo/Classified Proposals/{filename}.xlsx'
	# 	all_.to_excel(filename, index=False)
	# 	send_email(receiver=email, 
	# 			   subject='New Ways Of Work',
	# 			   body='This email is for NWOW', 
	# 			   attachment=filename)

	# styler = df.style.applymap(highlight_sla, subset=['SLA'])\
 #        			 .applymap(set_color, subset=['Area de Verificacao'])
	# styler.to_excel('formatted.xlsx', index=False)


def main():
	with open('creds.json') as f:
		data = json.loads(f.read())
		print(data)

# if __name__=='__main__':
# 	# split_proposal()
# 	files = glob('*.xlsx')
# 	for file in files:
# 		try:
# 			df = pd.read_excel(file)
# 			print(len(df['Nº'].unique()))
# 		except Exception as e:
# 			print(e)

	# main()



















































