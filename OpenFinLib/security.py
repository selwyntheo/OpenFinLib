import datetime
from dateutil.parser import parse

class SecurityRef:
	
	securities = [ {
	'securityid' : 12345,
	'securityidtype' : 'CUSIP',
	'assetclass' : 1,
	'securityclass' : 5,
	'securitytype' : 2,
	'country': 'USA',
	'countryoforigin': 'USA',
	'currency': 'USD',
	'settlement': 3,
	'daycount': 0,
	'fixedcoupon': 1,
	'coupon': 2.25,
	'frequency': 4,
	'issuedate' : parse('2015-10-02'),
	'firstcoupondate' : parse('2015-10-19'),
	'maturitydate': parse('2025-10-02')
	},
	{
	'securityid' : 12346,
	'securityidtype' : 'CUSIP',
	'assetclass' : 1,
	'securityclass' : 5,
	'securitytype' : 2,
	'country': 'USA',
	'countryoforigin': 'USA',
	'currency': 'USD',
	'settlement': 3,
	'daycount': 0,
	'fixedcoupon': 1,
	'coupon': 2.25,
	'frequency': 4,
	'issuedate' : parse('2015-6-25'),
	'firstcoupondate' : parse('2015-06-25'),
	'maturitydate': parse('2025-10-02')
	},
	{
	'securityid' : 12347,
	'securityidtype' : 'CUSIP',
	'assetclass' : 1,
	'securityclass' : 5,
	'securitytype' : 2,
	'country': 'USA',
	'countryoforigin': 'USA',
	'currency': 'USD',
	'settlement': 3,
	'daycount': 0,
	'fixedcoupon': 1,
	'coupon': 2.25,
	'frequency': 4,
	'issuedate' : parse('2015-10-02'),
	'firstcoupondate' : parse('2015-10-19'),
	'maturitydate': parse('2025-10-02')
	},
	{
	'securityid' : 12348,
	'securityidtype' : 'CUSIP',
	'assetclass' : 1,
	'securityclass' : 5,
	'securitytype' : 2,
	'country': 'USA',
	'countryoforigin': 'USA',
	'currency': 'USD',
	'settlement': 3,
	'daycount': 0,
	'fixedcoupon': 1,
	'coupon': 2.25,
	'frequency': 4,
	'issuedate' : parse('2015-10-02'),
	'firstcoupondate' : parse('2015-10-19'),
	'maturitydate': parse('2025-10-02')
	}]

	def __init__(self):
		self.data = []


	def get(self, securitytype, securityid):
		return (security for security in self.securities if security['securityid'] == securityid and security['securityidtype'] == securitytype).next()
