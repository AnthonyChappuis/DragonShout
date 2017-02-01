###############################################################################
#Author: 		Chappuis Anthony
#Filename: 		Track.py
#Application: 	DragonShout
#Date:			June 2014
#Description:	Contain the class for the tracks
#
#				Class Track:
#					_track_number as int
#						Class attribut containing the number of
#						instances
#					_name as string
#						Attribut containing the name of the track
#					_location as string
#						Attribut containing the physical location of the track
#						on the drive
#
#Modifications:
###############################################################################

class Track:
	"""Class Track:
			_track_number as int
				Class attribut containing the number of
				instances
			_name as string
				Attribut containing the name of the track
			_location as string
				Attribut containing the physical location of the track
				on the drive
	"""

	#class attribut
	_track_number = 0

	#class method
	def get_track_number(cls):
		"""This method gets the number of track available"""
		return cls._track_number
	get_track_number = classmethod(get_track_number)

	def unserialize(cls,data: dict):
		"""Used to unserialize JSON data for Track instances
		Takes one parameter:
		- data as dictionnary
		"""
		if "__class__" in data :
			if data["__class__"] == "Track":
				track_object = Track(data["name"],data["location"])
				return track_object
		return data
	unserialize = classmethod(unserialize)

	#constructor
	def __init__(self,name: str,location: str):
		self._name 		= name
		self._location 	= location
		#Bumping track number
		Track._track_number += 1

	#accessors
	def _get_name(self):
		return self._name

	def _get_location(self):
		return self._location

	#mutators
	def _set_name(self,new_name: str):
		self._name 		= new_name

	def _set_location(self,new_location: str):
		self._location 	= new_location

	#destructors
	def _del_name(self):
		del self._name

	def _del_location(self):
		del self._location

	#help
	def _help_name():
		return "Contains the track name for this program. Real filename from the operating system may be different"

	def _help_location():
		return "Contains the physical location of the track on the filesystem"

	#properties
	name 		= property(_get_name,		_set_name,		_del_name,		_help_name)
	location 	= property(_get_location,	_set_location,	_del_location,	_help_location)

	#method
	def serialize(self):
		"""Used to serialize instance datas to JSON format
		Takes no parameter
		"""
		return {"__class__": 	"Track",
				"name":			self.name,
				"location":		self.location}
