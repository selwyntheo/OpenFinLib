from workalendar.usa import *
from workalendar.europe import *
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import datetime
import calendar
from constants import DayCountConv, CalendarFactory
from oraclerepo import OracleRepo
from operator import itemgetter

class CSchedule:

	def __init__(self, config):
		self.record_no = 0
		self.config = config

	def get_sched(self, input):
		schedules= []
		lastDate = False
		if(self.validate_inputs(input) == True):
			securityType = input["SECURITYTYPE"]
			securityAlias = input["SECURITYALIAS"]
			datedDate = input["DATEDDATE"]
			nextCouponDate = input["NEXTCOUPONDATE"]
			prevCouponDate = input["PREVCOUPONDATE"]
			maturityDate = input["MATURITYDATE"]
			lastIncomeDate = input["LASTINCOMEDATE"]
			isoCountry = input["ISO"]
			frequency = input["FREQUENCY"]
			biz_day_conv = input["BUSINESSDAYCONVENTION"]
			day_count_conv = input["DAYCOUNTCONVENTION"]
			pikBond = input["PIKBOND"]
			coupon = input["COUPON"]
			currencyCode = input["CURRENCYCODE"]
			accrualMethod = input["ACCRUALMETHOD"]
			exdivdays = input["EX_DAYS"]
			aBond = input["ABOND"]
			vCoupon = input["VCOUPON"]
			vAmortization = input["VAMORTIZATION"]
			entityID =input["ENTITYID"]
			firstIncomeDate =input["FIRSTINCOMEDATE"]
			couponTypeCode = input["COUPONTYPECODE"]



			if exdivdays == None:
				exdivdays = 0

			if firstIncomeDate == self.last_day_of_month(firstIncomeDate) and lastIncomeDate==self.last_day_of_month(lastIncomeDate) and frequency[-1:] == "M":
				if accrualMethod != "SDM":
					lastDate = True
			
			"""  If it is a STEP bond calculate the coupon rate with the corresponding effective date """
			if couponTypeCode == 'S':
				result_rate = self.get_variable_step_rates(securityAlias)
				variable_rates = result_rate["data"]
				variable_rates = sorted(variable_rates, key=itemgetter('EFFECTIVE_DATE'), reverse=True)
				
			
					
			first = True
			
			while nextCouponDate <= lastIncomeDate:
				
				if(first):
					if couponTypeCode == 'S':
						coupon = self.get_variable_step_rate_coupon(prevCouponDate,variable_rates)
					
					couponPeriod = self.calculate_coupon_period(prevCouponDate,nextCouponDate,frequency,datedDate,lastIncomeDate,maturityDate,accrualMethod)
					coupon_rate = self.calculate_coupon_rate(coupon, prevCouponDate, None, nextCouponDate, frequency, day_count_conv,datedDate,lastIncomeDate,maturityDate,couponPeriod)
					
					if exdivdays >0:
						exdivdate = self.calculate_next_exdiv(nextCouponDate,exdivdays,isoCountry,currencyCode,day_count_conv)
					else:
						exdivdate = nextCouponDate
					schedules.append({
					'SecurityType' : securityType,
					'SecurityID' : input['SECURITYID'],
					'CouponPeriod': couponPeriod,
					'PreviousCouponDate': prevCouponDate,
					'NextCouponDate' : nextCouponDate,
					'exdivdays': exdivdays,
					'exdivdate': exdivdate,
					'AnnualCouponRate':coupon,
					'CouponRate' : coupon_rate,
					'BusinessDayConvention': biz_day_conv,
					'DayCountBasis': day_count_conv,
					'AccrualMethod' : accrualMethod,
					'PIKBond': pikBond,
					'ABond' : aBond,
					'VCoupon': vCoupon, 
					'VAmortization' : vAmortization,
					'SecurityAlias' : securityAlias,
					'EntityID': entityID
					})
					prevCouponDate = nextCouponDate
				else:
					if couponTypeCode == 'S':
						coupon = self.get_variable_step_rate_coupon(prevCouponDate,variable_rates)
					coupondate = self.calculate_next_coupon(nextCouponDate, frequency, biz_day_conv, isoCountry,lastDate)
					
					if biz_day_conv == "ADJROLL" or biz_day_conv == "ROLL":
						nextCouponDate = coupondate['act_coupon_date']
					else:
						nextCouponDate = coupondate['next_coupon_date']
					couponPeriod = self.calculate_coupon_period(prevCouponDate,nextCouponDate,frequency,datedDate,lastIncomeDate,maturityDate,accrualMethod)
					
					coupon_rate = self.calculate_coupon_rate(coupon, prevCouponDate, None, nextCouponDate, frequency, day_count_conv,datedDate,lastIncomeDate,maturityDate,couponPeriod)
					if exdivdays >0:
						exdivdate = self.calculate_next_exdiv(nextCouponDate,exdivdays,isoCountry,currencyCode,day_count_conv)
					else:
						exdivdate = nextCouponDate
					if nextCouponDate <= lastIncomeDate:
						schedules.append({
						'SecurityType' : securityType,
						'SecurityID' : input['SECURITYID'],
						'CouponPeriod': couponPeriod,
						'PreviousCouponDate': prevCouponDate,
						'NextCouponDate' : coupondate['next_coupon_date'],
						'exdivdays': exdivdays,
						'exdivdate': exdivdate,
						'AnnualCouponRate': coupon,
						'CouponRate' : coupon_rate,
						'BusinessDayConvention': biz_day_conv,
						'DayCountBasis': day_count_conv,
						'AccrualMethod' : accrualMethod,
						'PIKBond': pikBond,
						'ABond' : aBond,
						'VCoupon': vCoupon,
						'VAmortization' : vAmortization,
						'SecurityAlias' : securityAlias,
						'EntityID': entityID
						})

						prevCouponDate = coupondate['next_coupon_date']
						
				first = False
				

		if lastIncomeDate < maturityDate:
			if couponTypeCode == 'S':
				coupon = self.get_variable_step_rate_coupon(prevCouponDate,variable_rates)
			
			if exdivdays >0:
				exdivdate = self.calculate_next_exdiv(nextCouponDate,exdivdays,isoCountry,currencyCode,day_count_conv)
			else:
				exdivdate = nextCouponDate
			if exdivdate > maturityDate:
				exdivdate = maturityDate - relativedelta(days=exdivdays)
		
			if nextCouponDate != maturityDate:
				couponPeriod = self.calculate_coupon_period(prevCouponDate,maturityDate,frequency,datedDate,lastIncomeDate,None,accrualMethod)
			else:
				couponPeriod = self.calculate_coupon_period(prevCouponDate,nextCouponDate,frequency,datedDate,lastIncomeDate,maturityDate,accrualMethod)

			if nextCouponDate != maturityDate:
				coupon_rate = self.calculate_coupon_rate(coupon, prevCouponDate, None, maturityDate, frequency, day_count_conv,datedDate,lastIncomeDate,None,couponPeriod)
			else:
				coupon_rate = self.calculate_coupon_rate(coupon, prevCouponDate, None, nextCouponDate, frequency, day_count_conv,datedDate,lastIncomeDate,maturityDate,couponPeriod)	

				
			#print "Frequency %s" % frequency
			#print "Pervious Coupon Period %s" % prevCouponDate
			#print "Next Coupon Period %s" % nextCouponDate
			#print "Last Income Date %s" % lastIncomeDate
			#print "Maturity %s" % maturityDate
			#print "CouponPeriod of Last Period %s" % couponPeriod
			schedules.append({
				'SecurityType' : securityType,
				'SecurityID' : input['SECURITYID'],
				'CouponPeriod': couponPeriod,
				'PreviousCouponDate': prevCouponDate,
				'NextCouponDate' : maturityDate,
				'exdivdays': exdivdays,
				'exdivdate': exdivdate,
				'AnnualCouponRate': coupon,
				'CouponRate' : coupon_rate,
				'BusinessDayConvention': biz_day_conv,
				'DayCountBasis': day_count_conv,
				'AccrualMethod' : accrualMethod,
				'PIKBond': pikBond,
				'ABond' : aBond,
				'VCoupon': vCoupon,
				'VAmortization' : vAmortization,
				'SecurityAlias' : securityAlias,
				'EntityID': entityID
				})
		return schedules

	def get_variable_step_rates(self, securityAlias):
		query = None
		with open("step_rates.sql", "rw") as f:
			query = f.read()
			query = query % securityAlias
		return OracleRepo(self.config).run_query(query)


	def get_variable_step_rate_coupon(self, prevCouponDate, variable_rates):
		"""  Function to return the step rate of the coupon given a period  """
		for rates in variable_rates:
			if   prevCouponDate >= rates["EFFECTIVE_DATE"]:
				return rates["VARIABLE_RATE"]


	def validate_inputs(self, input):
		"""  do validations  """
		return True

	def calculate_coupon_period(self, prevCouponDate, nextCouponDate,freq,datedDate,lastIncomeDate,maturityDate,accrualMethod):
		"""  Calculate the difference between two periods  """
		if prevCouponDate == datedDate:
			if freq[-1:] == "M":
				months = int(freq[:-2])
				nextCouponDateCalc = prevCouponDate + relativedelta(months=months)
				if prevCouponDate == self.last_day_of_month(prevCouponDate):
					if accrualMethod =='LDM' or accrualMethod=='' or accrualMethod is None:
						nextCouponDateCalc=self.last_day_of_month(nextCouponDateCalc)
				if nextCouponDate != nextCouponDateCalc:
					couponPeriod =1
				else:
					couponPeriod =0
			elif freq[-1:] == "D":
				days = int(freq[:-2])
				nextCouponDateCalc = prevCouponDate + relativedelta(months=days)
				if nextCouponDate != nextCouponDateCalc:
					couponPeriod =1
				else:
					couponPeriod = 0
			elif freq[-1:] == "W":
				weeks = int(freq[:-2])
				nextCouponDateCalc = prevCouponDate + relativedelta(months=days)
				if nextCouponDate != nextCouponDateCalc:
					couponPeriod =1
				else:
					couponPeriod = 0
		elif nextCouponDate > lastIncomeDate and nextCouponDate != maturityDate:		
			if freq[-1:] == "M":
				months = int(freq[:-2])
				nextCouponDateCalc = prevCouponDate + relativedelta(months=months)
				if prevCouponDate == self.last_day_of_month(prevCouponDate):
					if accrualMethod =='LDM' or accrualMethod=='' or accrualMethod is None:
						nextCouponDateCalc=self.last_day_of_month(nextCouponDateCalc)
				if nextCouponDate != nextCouponDateCalc:
					couponPeriod =2
				else:
					couponPeriod = 0
			elif freq[-1:] == "D":
				days = int(freq[:-2])
				nextCouponDateCalc = prevCouponDate + relativedelta(months=days)
				if nextCouponDate != nextCouponDateCalc:
					couponPeriod =2
				else:
					couponPeriod = 0
			elif freq[-1:] == "W":
				weeks = int(freq[:-2])
				nextCouponDateCalc = prevCouponDate + relativedelta(months=weeks)
				if nextCouponDate != nextCouponDateCalc:
					couponPeriod =2
				else:
					couponPeriod = 0
		else:
			couponPeriod = 0
		return couponPeriod

	def calculate_next_exdiv(self,nextCouponDate,exdivdays,iso,currencyCode,day_count_conv):
		"""" This function removes the 31 day for SEK security"""
		if currencyCode == "SEK" and day_count_conv == DayCountConv.BASIC30E_360:
			exdivdate = nextCouponDate-relativedelta(days=exdivdays)
			for single_date in self.daterange(exdivdate, nextCouponDate):
				if single_date.day > 30:
					exdivdate = nextCouponDate -relativedelta(days=exdivdays+1)
		else:
			exdivdate = nextCouponDate-relativedelta(days=exdivdays)
		#cal = CalendarFactory().get(iso)
		#if exdivdate != None and not cal.is_working_day(exdivdate):
		#	exdivdate = self.get_prev_business_day(exdivdate,iso)
		return exdivdate

	def calculate_next_coupon(self, coupon_date, freq, biz_day_conv,iso,lastDate):
		next_coupon_date = None 
		if freq[-1:] == "M":
			months = int(freq[:-2])
			next_coupon_date = coupon_date + relativedelta(months=months)
		elif freq[-1:] == "D":
			days = int(freq[:-2])
			next_coupon_date = coupon_date + relativedelta(days=days)
		elif freq[-1:] == "W":
			weeks = int(freq[:-2])
			next_coupon_date = coupon_date + relativedelta(weeks=weeks)
		else:
			raise RuntimeError('Invalid coupon frequency: %s' % freq)

		cal = CalendarFactory().get(iso)

		biz_day = next_coupon_date
		if not cal.is_working_day(next_coupon_date):
			if biz_day_conv == "ADJMBC" or biz_day_conv == "MBC":
				biz_day = self.get_next_business_day(next_coupon_date,iso)
				if(biz_day.month != next_coupon_date.month):
					biz_day = self.get_prev_business_day(next_coupon_date,iso)
			elif biz_day_conv == "ADJFWD" or biz_day_conv == "FWD":
				biz_day = self.get_next_business_day(next_coupon_date,iso)
			elif biz_day_conv == "ADJBACK":
				biz_day = self.get_prev_business_day(next_coupon_date,iso)
			elif biz_day_conv == "ADJROLL" or biz_day_conv == "ROLL":
				biz_day =self.get_next_business_day(next_coupon_date,iso)
			else:
				#TODO: raise RuntimeError('Invalid business day convention: %s' % biz_day_conv)
				biz_day = next_coupon_date
		
		if lastDate == True:
			next_coupon_date = self.last_day_of_month(next_coupon_date)

		return {'next_coupon_date': next_coupon_date, 'act_coupon_date': biz_day}

	def calculate_coupon_rate(self, coupon, prevCouponDate, todayDate, nextCouponDate, frequency, day_count_conv,datedDate,lastIncomeDate,maturityDate,couponPeriod):

		days_factor = self.days_factor(prevCouponDate ,todayDate, nextCouponDate, day_count_conv,frequency,datedDate,lastIncomeDate,maturityDate,couponPeriod)
		if coupon == None:
			coupon_rate = 0
		else:
			coupon_rate = coupon * days_factor
		return coupon_rate


	def get_next_business_day(self, coupon_date,iso):
		cal = CalendarFactory().get(iso)
		next_day = coupon_date + relativedelta(days=1)
		while(not cal.is_working_day(next_day)):
			next_day = next_day + relativedelta(days=1)
		return next_day


	def get_prev_business_day(self, coupon_date,iso):
		cal = CalendarFactory().get(iso)
		prev_day = coupon_date - relativedelta(days=1)
		while(not cal.is_working_day(prev_day)):
			prev_day = prev_day - relativedelta(days=1)
		return prev_day

	def days_factor(self, prevCouponDate, todayDate,nextCouponDate,day_count_conv, frequency,datedDate,lastIncomeDate,maturityDate,couponPeriod):
		if day_count_conv == DayCountConv.ACT_ACT:
			freq = int(frequency[:-2])
			prevfreq_coupon_date = nextCouponDate + relativedelta(months=-freq)
			if couponPeriod == 1:
				num = (nextCouponDate-prevCouponDate).days
				dem = ((nextCouponDate-prevfreq_coupon_date).days * 12.0)/freq
				factor = num / dem
			elif couponPeriod == 0:
				factor = freq/12.0
			else:
				factor=1
		elif day_count_conv == DayCountConv.ACT_360:
			num = self.days_between(prevCouponDate,nextCouponDate)
			dem = 360 
			factor = num / dem
		elif day_count_conv == DayCountConv.ACT_365:
			num = self.days_between(prevCouponDate,nextCouponDate)
			dem = 365 
			factor = num / dem
		elif day_count_conv == DayCountConv.ACT_365L:
			num = self.days_between(prevCouponDate,nextCouponDate)
			if calendar.isleap(nextCouponDate.year):
				dem = 366
			else:
				dem = 365
			factor = num / dem
		elif day_count_conv == DayCountConv.ACT_252:
			if todayDate == None:
				num = self.days_between_actual(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between_actual(todayDate,nextCouponDate)
			dem = 252
			factor = num / dem

		elif day_count_conv == DayCountConv.BASIC30_360 or day_count_conv == None:
			if todayDate == None:
				num = self.days_between_actual(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between_actual(todayDate,nextCouponDate)
			dem = 360
			factor = num / dem

		elif day_count_conv == DayCountConv.BASIC30E_360:
			if todayDate == None:
				num = self.days_between_actual(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between_actual(todayDate,nextCouponDate)
			dem = 360
			factor = num / dem
		elif day_count_conv == DayCountConv.BASIC30_365:
			if todayDate == None:
				num = self.days_between_actual_plus(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between_actual_plus(todayDate,nextCouponDate)
			dem = 365
			factor = num / dem
		elif day_count_conv == DayCountConv.BASIC30E_365:
			if todayDate == None:
				num = self.days_between_actual(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between_actual(todayDate,nextCouponDate)
			dem = 365
			factor = num / dem
		elif day_count_conv == DayCountConv.CAD_365:
			if self.calculate_coupon_period(prevCouponDate,nextCouponDate,frequency,datedDate,lastIncomeDate,maturityDate,day_count_conv) !=0:
				num = self.days_between(prevCouponDate,nextCouponDate)
				dem = 365 
				factor = num / dem
			else:
				factor = 0.5
		elif day_count_conv == DayCountConv.JPY_365:
			if self.calculate_coupon_period(prevCouponDate,nextCouponDate,frequency,datedDate,lastIncomeDate,maturityDate,day_count_conv) !=0:
				num = self.days_between(prevCouponDate,nextCouponDate)
				dem = 365
				factor = num / dem
			else:
				factor = 0.5
				
		elif day_count_conv == DayCountConv.NL_365:
			freq = int(frequency[:-2])
			if couponPeriod == 1:
				num = self.days_between_nl(prevCouponDate,nextCouponDate)
				dem = 365 
				factor = num / dem
			elif couponPeriod == 0:
				factor = freq/12.0
			else:
				factor=1
		else:
			if todayDate == None:
				if frequency[-1] == "M":
					num = self.days_between_approx(prevCouponDate,nextCouponDate)
				else:
					num =self.days_between(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between_actual(todayDate,nextCouponDate)
			dem = 360
			factor = num / dem

		return factor


	def get_frequency_factor(self,freq):
		freq_factor = None
		if freq[-1:] == "M":
			months = int(freq[:-2])
			freq_factor = 12/ months 
		elif freq[-1:] == "D":
			days = int(freq[:-2])
			freq_factor = 365/ days
		elif freq[-1:] == "W":
			weeks = int(freq[:-2])
			freq_factor = 52 / weeks
		return freq_factor
	
	def last_day_of_month(self, any_day):
		next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
		return next_month - datetime.timedelta(days=next_month.day)

	def days_between(self, d1,d2):
		return (d2-d1).days * 1.0

	def days_between_nl(self, d1,d2):
		"""" This function removes the leap days"""
		if calendar.isleap(d1.year) or calendar.isleap(d2.year):
			if calendar.isleap(d1.year):
				leapDate = datetime.datetime(year=d1.year, month=2, day=29)
			elif calendar.isleap(d2.year):
				leapDate = datetime.datetime(year=d2.year, month=2, day=29)
			if d1 <= leapDate <= d2:
				days_between =(d2-d1).days * 1.0 -1
			else:
				days_between =(d2-d1).days *1.0
		else:
			days_between = (d2-d1).days * 1.0
		return days_between

	def days_between_actual(self, d1,d2):
		if d1.day >= 30:
			d1=datetime.datetime(d1.year,d1.month,30)
		if d2.day >=30:
			d2=datetime.datetime(d2.year,d2.month,30)
		return ((d2.year -d1.year)*360 + (d2.month - d1.month)*30 + (d2.day - d1.day)) * 1.0

	def days_between_actual_plus(self, d1,d2):
			if d1.day >= 30:
				d1=datetime.datetime(d1.year,d1.month,30)
				if d2.day >=30:
					d2=datetime.datetime(d2.year,d2.month,30)
			return ((d2.year -d1.year)*360 + (d2.month - d1.month)*30 + (d2.day - d1.day)) * 1.0


	def days_between_approx(self, d1,d2):
		return (abs((d2.year -d1.year)*360 +(d2.month - d1.month)*30 )) * 1.0


	def months_between(self, d1,d2):
		 return (d1.year - d2.year)*12 + d1.month - d2.month

	def weeks_between(self, d1,d2):
		return (d1-d2).days / 7

	def daterange(self, start_date, end_date):
		for n in range(int ((end_date - start_date).days)):
			yield start_date + timedelta(n)
