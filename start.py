#!/bin/python
import sys
import requests
import datetime
import os
from time import sleep
from pyquery import PyQuery
import re
import RPi_I2C_driver

while True:
	bot = requests.session()
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	bot.headers.update(headers)
	data = bot.get('https://dziekanat.agh.edu.pl/')
	pq = PyQuery(data.content)
	inputs = pq('input')
	input_arr = {}
	print inputs.items()
	for input in inputs.items():
		name = input.attr('name')
		value = ('' if input.attr('value') is None else input.attr('value'))
		input_arr[name] = value
	
	sleep(2)
	
	if(len(sys.argv) != 3):
		print 'Bledna liczba argumentow! Uzycie: python start.py IDENTYFIKATOR HASLO_DO_WD'
		exit()

	post_fields = input_arr
	post_fields['ctl00$ctl00$ContentPlaceHolder$MiddleContentPlaceHolder$txtIdent'] = sys.argv[1] # identyfikator
	post_fields['ctl00$ctl00$ContentPlaceHolder$MiddleContentPlaceHolder$txtHaslo'] = sys.argv[2] # haslo
	post_fields['ctl00$ctl00$ContentPlaceHolder$MiddleContentPlaceHolder$butLoguj'] = 'Zaloguj'
	post_fields['ctl00$ctl00$ContentPlaceHolder$MiddleContentPlaceHolder$rbKto'] = 'student'
	
	bot.post('https://dziekanat.agh.edu.pl/Logowanie2.aspx', post_fields)
	
	sleep(2)
	data = bot.get('https://dziekanat.agh.edu.pl/PodzGodzin.aspx')
	html = data.content
	pq = PyQuery(html)
	tag = pq('tr.gridDane')
	
	today = datetime.datetime.now()
	current_date = today.strftime('%d-%m-%Y')
	current_date_as_number = today.strftime('%d%m%Y')
	current_time = today.strftime('%H:%M')
	current_time_as_number = today.strftime('%H%M')
	
	
	
	
	
	mylcd = RPi_I2C_driver.lcd()
	if current_time_as_number < 600:
		mylcd.backlight(1)
	else:
		mylcd.backlight(0)
	
	
	
	for row in tag.items():
		td_date = row('td:first').contents()[0]	
		td_time = row('td:nth-child(2)').contents()[0]
		td_what = row('td:nth-child(4)').contents()[0]
		td_where = row('td:nth-child(6)').contents()[0]
		td_type = row('td:nth-child(8)').contents()[0]
		
		row_date = td_date
		td_date_short = re.sub('20', '', td_date)
		row_date_as_num = re.sub('[^0-9]','', td_date)
		row_time = td_time
		row_time_as_num= re.sub('[^0-9]','', td_time)
		
		td_where_short = re.sub('\s', '', td_where)
		
		if(int(row_date_as_num) == int(current_date_as_number)  and int(row_time_as_num) >= int(current_time_as_number)):
			displ_n_times = 10
			while(displ_n_times > 0):
				counter = 0
				while(counter < 8):
					if(len(td_what) < 8):
						mylcd.lcd_display_string_pos(td_what,1,1)
					else:
						mylcd.lcd_display_string_pos('        ',1,1)
						mylcd.lcd_display_string_pos(td_what[int(counter):(int(counter)+8)],1,1)
					if(counter % 6 == 0):
						mylcd.lcd_display_string_pos('               ',2,1)
						mylcd.lcd_display_string_pos(td_type,2,2)
						mylcd.lcd_display_string_pos(td_where_short,2,5)
					elif (counter % 3 == 0):
						mylcd.lcd_display_string_pos('               ',2,1)
						mylcd.lcd_display_string_pos(td_date,2,6)
					mylcd.lcd_display_string_pos(td_time,1,11)
					counter = counter + 1
					sleep(1)
				displ_n_times = displ_n_times - 1
			break;
		else:
			mylcd.lcd_display_string_pos('        ',1,1)
			mylcd.lcd_display_string_pos('Brak zajec',1,1)
			mylcd.lcd_display_string_pos('               ',2,1)
			mylcd.lcd_display_string_pos(td_date,2,6)
			sleep(56)
			pass
