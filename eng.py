from googletrans import Translator
from openpyxl import load_workbook
from random import randint
import eel
import pyttsx3

engine = pyttsx3.init()
translator = Translator()

eng = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'

engine.setProperty('voice', eng)
engine.setProperty("rate", 120)

wb = load_workbook('Eng.xlsx')
sheet = wb['Лист1']

english_words_sheet = sheet['A']
russian_words_sheet = sheet['B']
descriptions_sheet = sheet['C']

def get_random(args):
	random_values = []
	repeat = []
	i = 0
	while i <= len(args) - 1:
		random_number = randint(0, len(args) - 1)
		if str(random_number) in repeat:
			continue
		else:
			random_values.append(args[random_number])
			repeat.append(str(random_number))
		i += 1
	return random_values


def del_space(word:str):
	word = word.lstrip(' ')
	word = word.rstrip(' ')
	return word


eel.init('web')

@eel.expose
def voice(word):
	engine.say(word)
	engine.runAndWait()


@eel.expose
def get_word(slice_1, slice_2):	
	english_words = get_random(english_words_sheet[int(slice_1)-1:int(slice_2)+1])
	russian_words = get_random(russian_words_sheet[int(slice_1)-1:int(slice_2)+1])

	words_for_js = []
	translate_for_js = []
	eng_description_for_js = []
	rus_description_for_js = []

	quantity = int(slice_2) - int(slice_1) + 1
	i = 1

	while i <= quantity:
		if randint(0, 1) == 0:
			for word in english_words:
				row = word.row

				words_for_js.append(word.value)
				translate_for_js.append(sheet['B{}'.format(str(row))].value)
				eng_description_for_js.append(sheet['C{}'.format(str(row))].value)
				trans = translator.translate(
					str(sheet['C{}'.format(str(row))].value), dest='ru'
				).text

				if trans == 'Никто':
					rus_description_for_js.append('')

				else:
					rus_description_for_js.append(trans)

				english_words = english_words[1:]
				i += 1
				break

		else:
			for word in russian_words:
				row = word.row

				words_for_js.append(word.value)
				translate_for_js.append(sheet['A{}'.format(str(row))].value)
				eng_description_for_js.append(sheet['C{}'.format(str(row))].value)
				rus_description_for_js.append(translator.translate(
					str(sheet['C{}'.format(str(row))].value), dest='ru'
				).text)

				russian_words = russian_words[1:]
				i += 1
				break
	
	return [words_for_js, translate_for_js, eng_description_for_js, rus_description_for_js]

eel.start('eng.html', size=(700, 700))