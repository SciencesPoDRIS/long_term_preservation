#!/usr/bin/python
# -*- coding: utf-8 -*-


#
# External libs
#

import datetime


#
# Variables
#

# Dict used in translate_bequali_folder_name_filter function to get the folders name
bequali_folder_name = {
	'_meta' : 'Métadonnées',
	'add' : 'Documents additionnels',
	'admi' : 'Documents administratifs',
	'ana' : 'Analyse',
	'anal' : 'Analyse',
	'archives' : 'Archives',
	'col' : 'Collecte',
	'corresp' : 'Correspondance',
	'docu' : 'Documentation rassemblée en amont ou pendant terrain',
	'entretien' : 'Entretiens',
	'ese' : 'Enquête sur l\'enquête',
	'fiche' : 'Fiches',
	'methodo' : 'Méthodologie',
	'note'  : 'Notes',
	'outil' : 'Outil',
	'prep' : 'Préparation',
	'presse' : 'Presse / périodique',
	'rapport' : 'Rapports / synthèses',
	'transcr' : 'Transcription'
}
# Dict used in translate_bequali_folder_description_filter function to get the folders description
bequali_folder_description = {
	'_meta' : 'Dossier contenant les métadonnées xml et l\'inventaire des documents contenus dans le corpus.',
	'add' : 'Dossier contenant des documents conçus a posteriori de l\'enquête par l’équipe beQuali ou par les auteurs de l\'enquête.',
	'admi' : 'Dossier contenant des documents administratifs',
	'ana' : 'Dossier concernant tous les documents d\'analyse, de production et de communication scientifique, produits par les auteurs de l\'enquête.',
	'anal' : 'Dossier concernant tous les documents d\'analyse, de production et de communication scientifique, produits par les auteurs de l\'enquête.',
	'archives' : 'Dossier contenant des documents relatifs à la consultation d’archives ou d’aide à la compréhension de l’enquête',
	'col' : 'Dossier concernant tous les documents recueillis sur le terrain, collectés ou coproduits par les auteurs de l\'enquête.',
	'corresp' : 'Dossier contenant de la correspondance',
	'docu' : 'Dossier contenant la documentation rassemblée en amont ou pendant le terrain',
	'entretien' : 'Dossier contenant des documents relatifs aux entretiens',
	'ese' : 'Dossier contenant la production scientifique réalisée par l\'équipe beQuali ayant pour objet d’éclairer d\'un point de vue documentaire, méthodologique et analytique l\'enquête collectée et mise à disposition.',
	'fiche' : 'Dossier contenant des documents prenant la forme de fiche synthétique',
	'methodo' : 'Dossier contenant des documents relatifs à la méthodologie de l\'enquête',
	'note' : 'Dossier contenant des documents prenant la forme de notes manuscrites ou de notes d\'information',
	'outil' : 'Dossier contenant des documents concernant les outils utilisés (méthodologiques, etc.)',
	'prep' : 'Dossier concernant tous les documents préparant l’enquête.',
	'presse' : 'Dossier contenant des documents relatifs à la presse (coupure, dossier, journaux, etc)',
	'rapport' : 'Dossier contenant des documents prenant la forme de rapport écrit ou de synthèse',
	'transcr' : 'Dossier contenant les transcriptions d’entretiens'
}
# Dict used in bequali_mime_type_filter function to match file extension to a mimeType
mimeType = {
	'csv' : 'text/plain',
	'pdf' : 'application/pdf',
	'xml' : 'text/xml'
}

date_format = {
	1 : '%Y',
	2 : '%m/%Y',
	3 : '%d/%m/%Y'
}


#
# Functions
#

# Return the content of the first element
def first_filter(values) :
	return [values[0].text]

def type_filter(values) :
	return [type[str(values[0].text)]]

def concat_filter(values) :
	return [' '.join(value.text for value in values if value.text is not None)]

def filename_filter(values) :
	return [values[0].replace('file://', '').replace('ocr/', 'master/')]

def md5_filter(values) :
	# For a file, download it and return the MD5 checksum
	image_url = 'http://' + conf['ftp_server'] + conf['remote_path'] + '_'.join(values[0].split(folder_separator)[-1].split('_')[0:3]) + folder_separator + 'master' + folder_separator + values[0].split(folder_separator)[-1]
	image_path = values[0].replace('file://master/', conf['local_path'] + folder_separator + '_'.join(values[0].split(folder_separator)[-1].split('_')[0:3]) + folder_separator + 'DEPOT' + folder_separator + 'master' + folder_separator).replace('file://ocr/', conf['local_path'] + folder_separator + '_'.join(values[0].split(folder_separator)[-1].split('_')[0:3]) + folder_separator + 'DEPOT' + folder_separator + 'master' + folder_separator)
	if download_image(image_url, image_path) :
		return [md5(image_path)]

def md5xml_filter(values) :
	image_url = 'http://' + conf['ftp_server'] + conf['remote_path'] + values[0].text + folder_separator + values[0].text + '.xml'
	image_path = conf['local_path'] + folder_separator + values[0].text + folder_separator + 'DEPOT' + folder_separator + 'DESC' + folder_separator + values[0].text + '.xml'
	if download_image(image_url, image_path) :
		return [md5(image_path)]

def format_filter(values) :
	return [format[values[0].split('.')[-1]]]

def get_mets_file_filter(values) :
	return ['DESC/' + values[0].text + '.xml']

# Utils
def split_space_filter(values) :
	return values[0].text.split(' ')

# Utils
def split_underscore_filter(values) :
	return values[0].split('_')

# Utils
def get_first_element_filter(values) :
	return [values[0]]

# Utils
def get_fourth_element_filter(values) :
	return [values[3]]

# Utils
def lowercase_filter(values) :
	return [value.lower() for value in values]

def count_JPEG2000_filter(values) :
	return [str(len(values)) + ' documents JPG2000']

def count_PDF_filter(values) :
	return [str(len(values)) + ' documents PDF']

# Utils
def all_filter(values) :
	return [value.text for value in values]

# Utils
def min_filter(values) :
	return [min(values)]

def min_date_filter(values) :
	
	res = []
	format = {}
	for value in values :
		format[datetime.datetime.strptime(value, date_format[len(value.split('/'))])] = len(value.split('/'))
		res.append(datetime.datetime.strptime(value, date_format[len(value.split('/'))]))
	tmp = min(res)
	return [tmp.strftime(date_format[format[tmp]])]

# Utils
def max_filter(values) :
	return [max(values)]

def max_date_filter(values) :
	res = []
	format = {}
	for value in values :
		format[datetime.datetime.strptime(value, date_format[len(value.split('/'))])] = len(value.split('/'))
		res.append(datetime.datetime.strptime(value, date_format[len(value.split('/'))]))
	tmp = max(res)
	return [tmp.strftime(date_format[format[tmp]])]

# Archelec Filter
def plan_classement_filter(values) :
	# Project name
	plan_classement = u'Archives électorales/'
	identifier = values[0].text.split('_')
	# Add election type
	if identifier[1] == 'L' :
		plan_classement += u'Législatives/'
	elif identifier[1] == 'P' :
		plan_classement += u'Présidentielles/'
	else :
		logging.error('planClassement value is not supported : ' + identifier[1])
	# Add year
	plan_classement += identifier[2] + '/'
	# Add month
	plan_classement += identifier[3] + '/'
	# Add department
	plan_classement += identifier[4]
	return [plan_classement]

def current_date_filter():
	return str(datetime.date.today())

# BeQuali Filter
# Translate a key based on a dict
def translate_bequali_folder_name_filter(values) :
	try :
		res = [bequali_folder_name[values[0]].decode('UTF-8')]
	except KeyError :
		print "Error into function translate_bequali_folder_name_filter. Don't know how to translate name of : " + values[0]
		res = [values[0]]
	return res

# BeQuali Filter
# Translate a key based on a dict
def translate_bequali_folder_description_filter(values) :
	try :
		res = [bequali_folder_description[values[0]].decode('UTF-8')]
	except KeyError :
		print "Error into function translate_bequali_folder_description_filter. Don't know how to translate description of : " + values[0]
		res = [values[0]]
	return res

# BeQuali Filter
# Translate a key based on a dict
def bequali_type_filter(values) :
	return ['CDO']

# BeQuali Filter
# Return a mimeType according to the file extension
def bequali_mime_type_filter(values) :
	try :
		res = [mimeType[values[0].split('.')[-1]]]
	except KeyError :
		print "Error into function bequali_mime_type_filter. Don't know any mimeType for file extension : " + values[0]
		res = [values[0]]
	return res


# Archelec Filter
def format_fichier_filter(values) :
	if values[0] == 'image/jp2' :
		result = 'JPEG2000'
	elif values[0] == 'application/pdf' :
		result = 'PDF'
	else :
		logging.error('formatFichier value is not supported : ' + values[0])
	return [result]

# Archelec Filter
def nom_fichier_filter(values) :
	return ['/'.join(values[0].replace('file://', '').split('/')[2:])]

# Archelec Filter
def md5archelec_filter(values) :
	# For a file, download it into local path and return the MD5 checksum
	image_url = values[0].replace('file://', 'http://drd-archives01.sciences-po.fr/ArchivesArchElec/ELECTION%20LOT_00/LOT_00/').replace('.PDF', '.pdf').replace('.JP2', '.jp2').replace('.JPG', '.jpg')
	image_path = conf['local_path'] + folder_separator + values[0].split('/')[-1]
	if download_image(image_url, image_path) :
		return [md5(image_path)]
