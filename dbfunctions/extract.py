import json
import  re

from datetime import datetime

# Define input formats
input_formats = ['%d-%b-%Y', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%Y']

# Define output format
output_format = '%d/%m/%Y'

def format_date(date_str):
	for format_str in input_formats:
		try:
			date_obj = datetime.strptime(date_str, format_str)
			return date_obj.strftime(output_format)
			break
		except ValueError:
			pass

def contains_digits(s):
	return any(char.isdigit() for char in s)


def parser(data	):
	entities = {}
	
	expenseDocument=  data["ExpenseDocuments"][0]

	for field in expenseDocument['SummaryFields']:
		if field['Type']['Text'] == "INVOICE_RECEIPT_DATE":
			date_str = field['ValueDetection']['Text']
			date = format_date(date_str) 
			entities['date'] =  date

		if field['Type']['Text'] == "INVOICE_RECEIPT_ID": 
			entities['id'] = field['ValueDetection']['Text'] 

		if field['Type']['Text'] == "VENDOR_GST_NUMBER": 
			entities['v_gstin'] = field['ValueDetection']['Text'] 

		if field['Type']['Text'] == "RECEIVER_GST_NUMBER": 
			entities['r_gstin'] = field['ValueDetection']['Text'] 

		if field['Type']['Text'] == "RECEIVER_PHONE": 
			entities['r_phone'] = field['ValueDetection']['Text'] 

		if field['Type']['Text'] == "VENDOR_PHONE": 
			entities['v_phone'] = field['ValueDetection']['Text'] 

		if field['Type']['Text'] == "TOTAL": 
			if contains_digits(field['ValueDetection']['Text']):
				total = field['ValueDetection']['Text'] 
				# remove any non-digit characters
				deltable = "".join([i for i in total if i=="." or i.isdigit()])
				
				entities['total'] = int(float(deltable))

		if field['Type']['Text'] == "VENDOR_PAN_NUMBER": 
			entities['v_pan'] = field['ValueDetection']['Text'] 

		if field['Type']['Text'] == "RECEIVER_PAN_NUMBER": 
			entities['r_pan'] = field['ValueDetection']['Text'] 

		try :
			if field['GroupProperties'][0]['Types'][0] in ["RECEIVER" , "RECEIVER_BILL_TO"]:
				if field['Type']['Text'] == "NAME": 
					entities['r_name'] = field['ValueDetection']['Text'] 

				if field['Type']['Text'] == "STREET": 
					entities['r_street'] = field['ValueDetection']['Text'] 

				if field['Type']['Text'] == "CITY": 
					entities['r_city'] = field['ValueDetection']['Text'] 

				if field['Type']['Text'] == "STATE": 
					entities['r_state'] = field['ValueDetection']['Text'] 
				
				if field['Type']['Text'] == "COUNTRY": 
					entities['r_country'] = field['ValueDetection']['Text'] 
				
				if field['Type']['Text'] == "ZIP_CODE": 
					entities['r_zip'] = field['ValueDetection']['Text'] 
		except: pass 

		try :
			if field['GroupProperties'][0]['Types'][0] == "VENDOR":
				if field['Type']['Text'] == "NAME": 
					entities['v_name'] = field['ValueDetection']['Text'] 

				if field['Type']['Text'] == "STREET": 
					entities['v_street'] = field['ValueDetection']['Text'] 

				if field['Type']['Text'] == "CITY": 
					entities['v_city'] = field['ValueDetection']['Text'] 

				if field['Type']['Text'] == "STATE": 
					entities['v_state'] = field['ValueDetection']['Text'] 
				
				if field['Type']['Text'] == "COUNTRY": 
					entities['v_country'] = field['ValueDetection']['Text'] 
				
				if field['Type']['Text'] == "ZIP_CODE": 
					entities['v_zip'] = field['ValueDetection']['Text'] 
		except: pass 

	for field in expenseDocument['LineItemGroups'][0]['LineItems'][0]['LineItemExpenseFields']:
		
		try :
			if field['GroupProperties'][0]['Types'][0] == "OTHER":
				sno = re.compile(r'[No]')
				mo1 = sno.search(field['Type']['Text'])			
				if mo1 != None : 
					entities['sno'] = field['ValueDetection']['Text'] 
		except: pass 

		if field['Type']['Text'] == "ITEM":
			entities['i_item'] = field['ValueDetection']['Text']				
		if field['Type']['Text'] == "QUANTITY":
			en = field['ValueDetection']['Text']	
			deltable = "".join([i for i in en if i=="." or i.isdigit()])
			entities['l_qty'] = int(float(deltable))
		if field['Type']['Text'] == "UNIT_PRICE":
			en = field['ValueDetection']['Text']	
			deltable = "".join([i for i in en if i=="." or i.isdigit()])
			entities['l_uprice'] = int(float(deltable))
		if field['Type']['Text'] == "PRICE":
			en = field['ValueDetection']['Text']	
			deltable = "".join([i for i in en if i=="." or i.isdigit()])
			entities['l_total'] = int(float(deltable))

	return entities


