# This has the list of day counts and the related convention
from workalendar.usa import *
from workalendar.europe import *

class DayCountConv:
	ACT_ACT = "ACT/ACT"
	ACT_ACT_ISDA = "ACT/ACT(ISDA)"
	ACT_360 = "ACT/360"
	ACT_365 = "ACT/365"
	ACT_365L = "ACT/365L"
	ACT_252 = "ACT/252"

	BASIC30_360 = "BASIC30/360"
	NASD30_360 = "NASD30/360"

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

