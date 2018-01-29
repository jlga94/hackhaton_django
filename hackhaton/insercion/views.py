from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view, list_route, detail_route
from pymongo import MongoClient


# Create your views here.
class InsercionViewSet(viewsets.ModelViewSet):

	@list_route(methods=['post'], url_path='insertarDatos')
	def insercionDatos(self, request, pk=None):
		#print(request)
		#if request.method == 'POST':


		data_array = dict(request.data)
		print(data_array)

		keysInJSON = list(data_array.keys())

		keyName = keysInJSON[0]

		dataToInsert = data_array[keyName]


		client = MongoClient('localhost', 27017)


		db = client['BBVA']
		collection = db[keyName]
		collection.insert_one(dataToInsert)


		response = {"Insercion":"Ok"}

		return Response(response,status=status.HTTP_201_CREATED)