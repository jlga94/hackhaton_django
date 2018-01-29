from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view, list_route, detail_route
from pymongo import MongoClient
from bson import BSON
from bson import json_util
import json

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

	@list_route(methods=['post'], url_path='consultarDatos')
	def consultaDatos(self, request, pk=None):
		#print(request)
		#if request.method == 'POST':


		data_array = dict(request.data)
		print(data_array)


		tabla_name = data_array["Tabla"]



		client = MongoClient('localhost', 27017)


		db = client['BBVA']
		collection = db[tabla_name]
		datos = collection.find()
		print(datos)

		
		if tabla_name == "T005_PDTEPAGOS":
			datosAEntregar = []
			for row in datos:
				newData = {}
				#newData["cd_id_empresa"] = row["cd_id_empresa"]
				resultadosEmpresa = client['BBVA']["T001_Empresa"].find_one({"nu_id_entidad":row["cd_id_empresa"]})
				newData["cd_id_empresa"] = json.loads(json_util.dumps(resultadosEmpresa))



				resultadosDeudor = client['BBVA']["T004_Deudor"].find_one({"nu_id_deudor":row["cd_id_deudor"]})
				newData["cd_id_deudor"] = json.loads(json_util.dumps(resultadosDeudor))



				datosAEntregar.append(newData)
			response = {"Datos":datosAEntregar} 
		else:

			datosJSON = json.loads(json_util.dumps(datos))
			response = {"Datos":datosJSON}

		return Response(response,status=status.HTTP_201_CREATED)