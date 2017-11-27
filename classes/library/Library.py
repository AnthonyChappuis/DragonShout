###############################################################################
#Author: 		Chappuis Anthony
#Filename: 		Library.py
#Application: 	DragonShout
#Date:			June 2014
#Description:	Contain the class for handling the library file (saving and
#				loading)
#
#				Class Library:
#				_name as string
#					Contains the name of the library which also is the filename
#					on the drive
#				_categories as list
#					Contains the list of categories (instances of Category class)
#				_filepath as string
#					Contains the path to the library file on the drive
#
#Last edited: May 19th 2017
###############################################################################
import os
import json
from classes.library.Category import Category

class Library:
	"""Class Library:
		_name as string
			Contains the name of the library which also is the filename
			on the drive
		_categories as list
			Contains the list of categories
		_filepath as string
			Contains the path to the library file on the drive
	"""

	def load(cls,filepath: str):
		"""Used to load the library from the hard drive (JSON).
		Takes one parameter:
		- filepath as string
		"""
		try :
			with open(filepath, "r", encoding="utf-8") as json_file:
				library_object = json.load(json_file, object_hook=cls.unserialize)

			library_object.filepath = filepath
			return library_object
		except :
			return False
	load = classmethod(load)

	#class method
	def unserialize(cls, data: dict):
		"""Used to unserialize json data to set Library instance attributs and create Category
		class instances.
		Takes two parameters:
		- data as dictionnary
		- filepath as string
		"""
		if "__class__" in data :
			if data["__class__"] == "Library":
				#creating Library instance
				library_object = Library(data["name"],"")

				#unserializing categories for this library
				category_list = []
				for category in data["categories"]:
					category_list.append(Category.unserialize(category))
				library_object.categories = category_list

				return library_object

			return data
	unserialize = classmethod(unserialize)

	#constructor
	def __init__(self,name:str, filepath: str):
		self._name			= name
		self._filepath 		= filepath
		self._categories 	= []

	#accessors
	def _get_name(self):
		return self._name

	def _get_filepath(self):
		return self._filepath

	def _get_categories(self):
		return self._categories

	#mutators
	def _set_name(self, new_name: str):
		self._name 			= new_name

	def _set_filepath(self, new_filepath: str):
		self._filepath 		= new_filepath

	def _set_categories(self,categories: list):
		self._categories 	= categories

	#destructors
	def _del_name(self):
		del self._name

	def _del_filepath(self):
		del self._filepath

	def _del_categories(self):
		del self._categories

	#help
	def _help_name():
		return "Contains the name of the library which also is the filename on the drive"

	def _help_filepath():
		return "Contains the filepath to the library file"

	def _help_categories():
		return "Contains the list of categories"

	#properties
	name 		= property(_get_name,			_set_name,			_del_name,			_help_name)
	filepath 	= property(_get_filepath,		_set_filepath,		_del_filepath,		_help_filepath)
	categories 	= property(_get_categories,		_set_categories,	_del_categories,	_help_categories)

	#methods
	def add_category(self,name: str, iconPath: str=''):
		"""Used to add a category to the library.
		Takes one parameter:
		- name as string
		"""
		self._categories.append(Category(name,iconPath))

	def get_category(self,name: str):
		"""Used to get a specific category from the library.
		Takes one parameter:
		- name as string
		"""
		for category in self.categories:
			if category.name == name:
				return category

		return False

	def gather_library(self):
		"""Used to gather the categories and tracks for this library.
		Takes no parameter
		Returns one dictionnary containing the lists of tracks:
		[category1 => [track,track,track],category2 = >[track]]
		"""
		library = {}
		for category in self.categories:
			track_list = []
			for track in category.tracks:
				track_list.append(track.name)

			library[category.name] = track_list

		return library

	#file handling
	def save(self,filepath:str='./new_library.json'):
		"""Used to save the library on the hard drive (JSON).
		Takes one parameters:
		- filepath as string
		"""
		self.filepath = filepath

		#if the file doesn't exist, create it
		if not(os.path.isfile(filepath)):
			open(filepath,"x", encoding="utf-8")

		with open(filepath,"w", encoding="utf-8") as json_file:
			json.dump(self.serialize(),json_file, indent=4)

	def serialize(self):
		"""Used to serialize instance data to JSON format
		toakes no parameter.
		"""
		category_list = []
		for category in self.categories:
			category_list.append(category.serialize())

		return {"__class__": 	"Library",
				"name":			self.name,
				"categories":	category_list}
