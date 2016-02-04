# This has the list of day counts and the related convention
from workalendar.usa import *
from workalendar.europe import *

class DayCountConv:
	ACT_ACT = "ACT/ACT"
	ACT_ACT_ISDA = "ACT/ACT(ISDA)"

class CalendarFactory:

	def __init__(self):
		self.map = {
			"USA": "UnitedStates",
			"FRA": "France",
			"GRE": "Greece",
			"GBR": "UnitedKingdom"
		}

	def get(self, countryISO):
		return eval("%s()" % self.map[countryISO])

