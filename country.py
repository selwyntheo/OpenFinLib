import datetime
from dateutil.parser import parse

class Country:
	countries = [ {
	'countryiso' : USA,
	'countryname' : 'United States'},
	{
	'countryiso' : FRA,
	'countryname' : 'France'},
	{
	'countryiso' : GRE,
	'countryname' : 'Greece'},
	{
	'countryiso' : GBR,
	'countryname' : 'United Kingdom'}
	 ]

	def __init__(self):
		self.data = []

	def get(self, countryiso):
		return (country for country in self.countries if country['countryiso'] == countryiso).next()
