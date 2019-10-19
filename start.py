import requests
import datetime
from time import sleep
from pyquery import PyQuery    
import re

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


post_fields = input_arr
post_fields['ctl00$ctl00$ContentPlaceHolder$MiddleContentPlaceHolder$txtIdent'] = '' # identyfikator
post_fields['ctl00$ctl00$ContentPlaceHolder$MiddleContentPlaceHolder$txtHaslo'] = '' # haslo
post_fields['ctl00$ctl00$ContentPlaceHolder$MiddleContentPlaceHolder$butLoguj'] = 'Zaloguj'
post_fields['ctl00$ctl00$ContentPlaceHolder$MiddleContentPlaceHolder$rbKto'] = 'student'

#print post_fields
#print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
bot.post('https://dziekanat.agh.edu.pl/Logowanie2.aspx', post_fields)

sleep(2)
data = bot.get('https://dziekanat.agh.edu.pl/PodzGodzin.aspx')
html = data.content
pq = PyQuery(html)
tag = pq('tr.gridDane')

#print html
today = datetime.datetime.now()
current_date = today.strftime('%d-%m-%Y')
current_date_as_number = today.strftime('%d%m%Y')
current_time = today.strftime('%H:%M')
current_time_as_number = today.strftime('%H%M')


print '=-=-=-=-=-=-=-=-=-=-=-=-='
for row in tag.items():
	td_date = row('td:first').contents()[0]	
	td_time = row('td:nth-child(2)').contents()[0]
	td_what = row('td:nth-child(4)').contents()[0]
	td_where = row('td:nth-child(6)').contents()[0]

	row_date = td_date
	row_date_as_num = re.sub('[^0-9]','', td_date)
	row_time = td_time
	row_time_as_num= re.sub('[^0-9]','', td_time)

	if(int(row_date_as_num) == int(current_date_as_number) - 3000000 and int(row_time_as_num) >= int(current_time_as_number)-2000):
		print row_date
		print row_time
		print td_what
		print td_where
		break;
	else:
		pass


	
