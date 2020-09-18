from openpyxl import *
import webbrowser


wb = load_workbook('Eng.xlsx')
sheet = wb['Лист1']

english_words = list(sheet['A'])
transcription = list(sheet['B'])


for word in transcription:
	if str(type(word.value)) == "<class 'NoneType'>":
		english_word = sheet['A{}'.format(str(word.row))]
		russian_word = sheet['C{}'.format(str(word.row))]
		link = 'https://www.ldoceonline.com/search/english/direct/?q={}'.format(english_word.value)
		print(english_word.value + ' - ' + russian_word.value)
		webbrowser.open(link, new=1)
		inp = input('Введите транскрипцию: ')
		sheet.cell(row=word.row, column=2).value = inp
		wb.save("Eng.xlsx")
		print('Мы записали транскрипцию в Ваш excel файлик')
		print('-------------------------------------------')
	else:
		continue