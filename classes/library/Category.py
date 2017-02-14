###############################################################################
#Author: 		Chappuis Anthony
#Filename: 		Category.py
#Application: 	DragonShout
#Date:			June 2014
#Description:	Contain the class for the musics(tracks) categories
#
#				Class Category:
#					_category_number as int
#						Class attribut containing the number of
#						instances
#					_name as string
#						Attribut containing the name of the category
#					_tracks as list
#						Attribut containing the list of tracks for the category
#
#Modifications:
###############################################################################

from classes.library.Track import Track

class Category:
	"""Class Category:
		_category_number as int
			Class attribut containing the number of
			instances
		_name as string
			Attribut containing the name of the category
		_tracks as list
			Attribut containing the list of tracks for the category
	"""

	#class attribut
	_category_number 	= 0

	#class method
	def get_category_number(cls):
		"""This method gets the number of category available"""
		return cls._category_number
	get_category_number = classmethod(get_category_number)

	def unserialize(cls,data: dict):
		"""Used to unserialize JSON data for Category instances
		Takes one parameter:
		- data as dictionnary
		"""
		if "__class__" in data :
			if data["__class__"] == "Category":
				#Creating Category instance
				category_object = Category(data["name"])

				#unserializing tracks for this category
				track_list = []
				for track in data["tracks"]:
					track_list.append(Track.unserialize(track))
				category_object.tracks = track_list

				return category_object
			return data
	unserialize = classmethod(unserialize)

	#constructor
	def __init__(self,name: str):
		self._name = name
		self._tracks = []
		#Bumping category number
		Category._category_number += 1
		
	#accessors
	def _get_name(self):
		return self._name

	def _get_tracks(self):
		return self._tracks

	#mutators
	def _set_name(self,new_name: str):
		self._name = new_name

	def _set_tracks(self,new_track: Track):
		self._tracks = [new_track]

	#destructors
	def _del_name(self):
		del self._name

	def _del_tracks(self):
		del self._tracks

	#help
	def _help_name():
		return "Contains the category name"

	def _help_tracks():
		return "contains the list of tracks for the given category"

	#properties
	name = property(_get_name,		_set_name,		_del_name,		_help_name)
	tracks = property(_get_tracks,	_set_tracks,	_del_tracks,	_help_tracks)

	#methods
	def add_track(self,name: str,location: str):
		"""Used to add a track to the category.
		Takes two parameter:
		- name as string
		- location as string
		"""
		self._tracks.append(Track(name,location))

	def remove_track(self,track: Track):
		"""Used to remove a track from the category.
		Takes one parameter:
		- new_track as Track object
		"""
		self.tracks.remove(track)

	def serialize(self):
		"""Used to serialize instance datas to JSON format
		Takes no parameter
		"""
		track_list = []
		for track in self.tracks:
			track_list.append(track.serialize())

		return {"__class__": 	"Category",
				"name":			self.name,
				"tracks":		track_list}
