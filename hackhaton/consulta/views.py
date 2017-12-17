from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view, list_route, detail_route
import csv,string, re
from nltk.stem.snowball import SpanishStemmer
from nltk.corpus import stopwords
from collections import Counter
import unicodedata

spanishStemmer = SpanishStemmer()

'''def readCSV():
    with open('static/Lista-de-palabras.csv') as csvfile:
        reader = csv.DictReader(csvfile,dialect='excel')
        fisica = set()
        psicologica = set()
        economica = set()
        sexual = set()
        for row in reader:
            fisica.add(row['Violencia Física'])
            psicologica.add(row['Violencia Psicológica'])
            economica.add(row['Violencia económica o patrimonial'])
            sexual.add(row['Violencia sexual'])
        fisica.discard('')
        psicologica.discard('')
        economica.discard('')
        sexual.discard('')
        a = {}
        a['Violencia Física'] = fisica
        a['Violencia Psicológica'] = psicologica
        a['Violencia económica o patrimonial'] = economica
        a['Violencia sexual'] = sexual
        return a'''

def readCSV():
    with open('static/Lista-de-palabras.csv') as csvfile:
        reader = csv.DictReader(csvfile,dialect='excel')
        legal = set()
        psicologica = set()
        for row in reader:
        	textLegal = row['Legal']
        	if textLegal != None:
        		listWordsLegal = textLegal.split()
        		for word in listWordsLegal:
        			#legal.add(word)
        			legal.add(spanishStemmer.stem(word))


        	textPsicologica = row['Psicologica']
        	if textPsicologica != None:
        		listWordsPsicologica = textPsicologica.split()
        		for word in listWordsPsicologica:
        			#psicologica.add(word)
        			psicologica.add(spanishStemmer.stem(word))

            #legal.add(row['Legal'])
            #psicologica.add(row['Psicologica'])

        legal.discard('')
        psicologica.discard('')

        a = {}
        a['Legal'] = legal
        a['Psicologica'] = psicologica
        return a

def remove_numbers(text):
	return ''.join([letter for letter in text if not letter.isdigit()])

def remove_punctuation(text):
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	return regex.sub(' ', text)

def strip_accents(s):
	return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def removeStopwordsInList(text):
	stopwords_sp_nltk = set(stopwords.words('spanish'))

	additionalStopwordsSpanish = {'u','y/o','año','años','alto','ser','etc','respecto','hacer','tal','dentro','mes','meses','tener','experiencia','trabajo','bueno','afín','afine',
        'nivel','pequeño','haber','menos','menor','deseable','incluir','pues','parte','manera','según','lunes','martes','miércoles','jueves','viernes','sábado','domingo','lugar','fondo',
        'enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre','asi','así','través','uno','uso','casa','mismo','mediante','gran',
        'grande','hacia','conforme','número','siguiente','link','cuatro','tres','cinco','sitio','lista','anual','mensual','trimestral','bimestral','semestral','semanal','diario','día'}
	stopSpanish = stopwords_sp_nltk.union(additionalStopwordsSpanish)

	return [spanishStemmer.stem(word) for word in text.split() if word not in stopSpanish]
	#return [word for word in text.split() if word not in stopSpanish]

def preprocessText(text):

	text=text.lower()
	text = strip_accents(text)
	text = remove_numbers(text)
	text = remove_punctuation(text)
	listWords = removeStopwordsInList(text)

	return listWords

# Create your views here.
class ConsultaViewSet(viewsets.ModelViewSet):


	@list_route(methods=['post'], url_path='consultaTipoServicio')
	def consultaTipoViolencia(self, request, pk=None):
		data_array = dict(request.data)
		#print(data_array)

		testimonioText = data_array['testimonio'][0]
		print(testimonioText)
		listWords = set(preprocessText(testimonioText))
		print(listWords)

		lista = readCSV()
		legal = lista['Legal']
		psicologica = lista['Psicologica']

		print("Total Legal: " + str(len(legal)))
		print("Total Psicologica: " + str(len(psicologica)))

		numWordsLegal = 0
		for wordLegal in legal:
			if wordLegal in listWords:
				numWordsLegal += 1

		numWordsPsicologica = 0
		for wordPsicologica in psicologica:
			if wordPsicologica in listWords:
				numWordsPsicologica += 1

		print("Legal: " + str(numWordsLegal))
		print("Psicologica: " + str(numWordsPsicologica))


		totalEncontrados = numWordsLegal + numWordsPsicologica

		response = {}

		if totalEncontrados > 0:
			porcLegal = numWordsLegal / totalEncontrados
			porcPsicologica = numWordsPsicologica / totalEncontrados


			response['legal'] = porcLegal
			response['psicologico'] = porcPsicologica

		else:
			response['legal'] = 0
			response['psicologico'] = 0


		return Response(response,status=status.HTTP_201_CREATED)