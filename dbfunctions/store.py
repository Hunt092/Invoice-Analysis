
"""
{'r_street': '1087/B, HKM Road, Model Colony, Shivaji Nagar,', 'r_city': 'Pune', 
'r_state': 'Maharastra', 'r_zip': '411016', 'r_name': 'M/S C. C. Engineers Pvt.Ltd', 'r_gstin': '27AAACC7557P1Z1',

'v_street': '155, Juhi', 'v_city': ',Kanpur', 'v_name': '*DEVI CONSTRUCTIONS*', 
'v_phone': '8604343361' 'v_gstin': '09BGPPT7730J1ZK',

'date': '16/06/2021', 'id': 'DC/21-22/010','total': '42952.00'

'i_item': 'Ready Mix Concrete -M 25', 'l_qty': '7', 'l_uprice': '5200.00', 'l_total': '42952.00'}
"""

def store(entities, conn):
	cursor = conn.cursor()

	#if reciever not in dimension table then insert record
	r_name = entities['r_name']
	cursor.execute('''SELECT receiver_id from receiver_details WHERE name = '{}' '''.format(r_name))
	if cursor.fetchone() == None: 
		if 'r_street' in entities.keys() : r_street = entities['r_street'] 
		else : r_street = ''
		if 'r_city' in entities.keys() : r_city = entities['r_city'] 
		else : r_city = ''
		if 'r_state' in entities.keys() : r_state = entities['r_state']
		else : r_state = ''
		if 'r_country' in entities.keys()  : r_country = entities['r_country'] 
		else : r_country = ''
		if 'r_zip' in entities.keys() : r_zip = entities['r_zip']
		else: r_zip = ''
		if 'r_phone' in entities.keys() : r_phone = entities['r_phone']
		else : r_phone = ''
		if 'r_gstin' in entities.keys() : r_gstin = entities['r_gstin']
		else : r_gstin = ''
		if 'r_pan' in entities.keys() : r_pan = entities['r_pan']
		else : r_pan = ''
		cursor.execute('''INSERT INTO receiver_details( street ,city ,	state, country, zip_code ,name , phone, gstin, pan)
		VALUES ('{}','{}','{}','{}', '{}', '{}', '{}', '{}', '{}')'''.format( r_street ,r_city ,r_state,r_country, r_zip ,r_name ,r_phone,  r_gstin , r_pan))
		conn.commit()

		cursor.execute('''SELECT receiver_id from receiver_details WHERE name = '{}' '''.format(r_name))
		receiver_id = cursor.fetchone()[0]  
		#print("rid in new: ", receiver_id) 
	else :
		cursor.execute('''SELECT receiver_id from receiver_details WHERE name = '{}' '''.format(r_name))
		receiver_id = cursor.fetchone()[0]   
		#print("rid in old: ", receiver_id)
	

	#if vendor not in dimension table then insert record
	v_name = entities['v_name']
	cursor.execute('''SELECT vendor_id from vendor_details WHERE name = '{}' '''.format(v_name))
	if cursor.fetchone() == None: 
		if 'v_street' in entities.keys() : v_street = entities['v_street'] 
		else : v_street = ''
		if 'v_city' in entities.keys() : v_city = entities['v_city'] 
		else : v_city = ''
		if 'v_state' in entities.keys() : v_state = entities['v_state']
		else : v_state = ''
		if 'v_country' in entities.keys()  : v_country = entities['v_country'] 
		else : v_country = ''
		if 'v_zip' in entities.keys() : v_zip = entities['v_zip']
		else: v_zip = ''
		if 'v_phone' in entities.keys() : v_phone = entities['v_phone']
		else : v_phone = ''
		if 'v_gstin' in entities.keys() : v_gstin = entities['v_gstin']
		else : v_gstin = ''
		if 'v_pan' in entities.keys() : v_pan = entities['v_pan']
		else : v_pan = ''
		cursor.execute('''INSERT INTO vendor_details( street ,city ,state, country, zip_code ,name , phone, gstin, pan)
		VALUES ('{}','{}','{}','{}', '{}', '{}', '{}', '{}', '{}')'''.format( v_street ,v_city ,v_state,v_country, v_zip ,v_name ,v_phone,  v_gstin , v_pan))
		conn.commit()

		cursor.execute('''SELECT vendor_id from vendor_details WHERE name = '{}' '''.format(v_name))
		vendor_id = cursor.fetchone()[0]  
		 
	else :
		cursor.execute('''SELECT vendor_id from vendor_details WHERE name = '{}' '''.format(v_name))
		vendor_id = cursor.fetchone()[0]   
		


	if 'date' in entities.keys() : date = entities['date']
	else : date =  ''
	if 'id' in entities.keys() : id = entities['id']
	else : id = ''
	if 'total' in entities.keys() : total = entities['total']
	else : total = 0
	cursor.execute('''INSERT INTO invoice_details(receiver_id, vendor_id, order_date, invoice_recipt_id, total)
	 VALUES ({}, {}, '{}', '{}', {})'''.format(receiver_id, vendor_id, date, id , total))
	conn.commit()
	cursor.execute('''SELECT invoice_id from invoice_details WHERE invoice_recipt_id = '{}' '''.format(id))
	invoice_id = cursor.fetchone()[0]



	#'i_item': 'Ready Mix Concrete -M 25', 'l_qty': '7', 'l_uprice': '5200.00', 'l_total': '42952.00'

	if 'i_item' in entities.keys() : item_description = entities['i_item']
	else : item_description =  ''
	if 'l_qty' in entities.keys() : quantity = entities['l_qty']
	else : quantity = 0
	if 'l_uprice' in entities.keys() : product_price = entities['l_uprice']
	else : product_price = 0
	if 'l_total' in entities.keys() : total_price = entities['l_total']
	else : total_price = 0

	if 'sno' in entities.keys() : serial_number = entities['sno']
	else : serial_number = 0
	if 'product_code' in entities.keys() : product_code = entities['product_code']
	else : product_code = 0
	if 'additional_amount' in entities.keys() : additional_amount = entities['additional_amount']
	else : additional_amount = 0
	cursor.execute('''INSERT INTO line_item_details(invoice_id, serial_number, item_description, product_code, 
		quantity, additional_amount, product_price, total_price)
		VALUES ({}, {}, '{}', '{}', {}, {}, {}, {})'''.format(invoice_id, serial_number, item_description,
							product_code, quantity, additional_amount, product_price, total_price))
	conn.commit()

	print("Records inserted........")

	# Closing the connection




# fpath = r'C:/Users/Dell/Downloads/BEProject/expenseAPIoutput/10-Devi construction.json'
# entity = parser(fpath)
# #print(entity)
# store(entity, conn)



getexpsensewithyearandmonth="""
SELECT
  EXTRACT(MONTH FROM TO_DATE(order_date, 'DD/MM/YYYY')) AS month,
  EXTRACT(YEAR FROM TO_DATE(order_date, 'DD/MM/YYYY')) AS year,
  SUM(total) AS total_per_month
FROM
  public.invoice_details
GROUP BY
  EXTRACT(MONTH FROM TO_DATE(order_date, 'DD/MM/YYYY')),
  EXTRACT(YEAR FROM TO_DATE(order_date, 'DD/MM/YYYY'))
ORDER BY
  year DESC,
  month DESC;
  """