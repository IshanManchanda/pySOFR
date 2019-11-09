from os import environ

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openpyxl import Workbook
from requests import Session

load_dotenv()

SCHOOL_CODE = environ.get('SCHOOL_CODE', input('Enter School Code: '))
SECTIONS = 'FGHIJKLM'
STUDENTS_PER_SECTION = 40
LAST_VALID_ROLL = '000'
ROLLS = ['00' + str(x) if x > 9 else '0' + str(x) for x in range(1, 100)]

BASE_URL = 'http://results.sofworld.org/results'


def request(section, roll_number):
	session = Session()
	a = session.get(BASE_URL)
	data = get_form_data(a, section, roll_number)

	a = session.post(BASE_URL, data)
	url = a.headers['Link'].split(">")[0][1:]
	if url == BASE_URL:
		return False, None

	return process_result(session.get(url))


def get_form_data(a, section, roll_number):
	soup = BeautifulSoup(a.text, 'html.parser')
	input_fields = soup.find_all('input')
	captcha = soup.find('span', ['field-prefix']).text.split(' ')[:-2]

	s_id = input_fields[4]['value']
	token = input_fields[5]['value']
	build_id = input_fields[8]['value']

	ans = 0
	if captcha[1] == u'+':
		ans = int(captcha[0]) + int(captcha[2])
	elif captcha[1] == u'-':
		ans = int(captcha[0]) - int(captcha[2])
	else:
		print(f'Unable to solve captcha! Question: {captcha}')
		exit(1)

	return {
		'olympiad_selected': 'c1',
		'rollid1': SCHOOL_CODE,
		'rollid2': '11',
		'op': 'View+Results',
		'form_id': 'ac_result_cards_enter_rollid_form',
		'rollid3': section,
		'rollid4': roll_number,
		'captcha_sid': s_id,
		'captcha_token': token,
		'captcha_response': ans,
		'form_build_id': build_id
	}


def process_result(a):
	soup = BeautifulSoup(a.text, 'html.parser')
	data = soup.find_all('td')

	if len(data) == 0:
		return False, None

	return True, {
		'name': data[1].text,
		'roll': data[3].text,
		'section': data[7].text,
		'marks': data[9].text.split("/")[0].strip(),
		'international': data[11].text,
		'zonal': data[15].text,
		'school': data[19].text
	}


def next_roll(section, roll_number, x, error):
	roll_number += 1
	if not x:
		error += 1
	else:
		error = 0

	if error > 40:
		roll_number -= 41
		section += 1
		error = 0
	return section, roll_number, error


def main():
	section = roll_number = error = 0

	book = Workbook()
	NCO_sheet = book.active
	NCO_sheet.title = 'NCO'

	NCO_sheet.append([
		'Name',
		'Roll Number',
		'Section',
		'Marks',
		'International Rank',
		'Zonal Rank',
		'School Rank'
	])

	while section < len(SECTIONS):
		x, result = request(
			SECTIONS[section],
			roll_number if roll_number > 98 else ROLLS[roll_number]
		)

		if x:
			print(result['name'], result['marks'])
			NCO_sheet.append([
				result['name'],
				result['roll'],
				result['section'],
				result['marks'],
				result['international'],
				result['zonal'],
				result['school']
			])
		section, roll_number, error = next_roll(section, roll_number, x, error)
	book.save('Results: NCO.xlsx')


if __name__ == '__main__':
	main()
