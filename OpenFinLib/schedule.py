from workalendar.usa import *
from workalendar.europe import *
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from datetime import datetime
import calendar
from constants import DayCountConv, CalendarFactory

class CSchedule:
	def get_schedule(self,security):
		frequency_months = 12/security['frequency']
		coupondate = security['firstcoupondate']
		while coupondate < security['maturitydate']:
			cal = UnitedStates()
			if cal.is_holiday(coupondate):
				print('%s coupondate is holiday' % str(coupondate))
			yield { 'date': coupondate, 'coupon': security['coupon'] }
			coupondate = coupondate + relativedelta(months=frequency_months)



	def get(self, input):
		schedules= []
		if(self.validate_inputs(input) == True):
			nextCouponDate = parse(input["nextCouponDate"])
			prevCouponDate = parse(input["prevCouponDate"])
			maturityDate = parse(input["maturityDate"])
			isoCountry = input["iso"]
			frequency = input["frequency"]
			biz_day_conv = input["businessDayConvention"]
			day_count_conv = input["dayCountConvention"]
			coupon = float(input["coupon"])

			first = True
			while nextCouponDate < maturityDate:
				coupondate = self.calculate_next_coupon(nextCouponDate, frequency, biz_day_conv,isoCountry)
				if biz_day_conv == "ADJROLL" or biz_day_conv == "ROLL":
					nextCouponDate = coupondate['act_coupon_date']
				else:
					nextCouponDate = coupondate['next_coupon_date']
				if(first):
					coupon_rate = self.calculate_coupon_rate(coupon,prevCouponDate, datetime.now(), nextCouponDate, frequency,day_count_conv)
				else:
					coupon_rate = self.calculate_coupon_rate(coupon,prevCouponDate, None, nextCouponDate, frequency,day_count_conv)
				schedules.append({
					'SecurityID' : input['securityId'],
					'PrevCouponDate': prevCouponDate,
					'CouponDate' : coupondate['act_coupon_date'],
					'Coupon' : coupon_rate
					})
				prevCouponDate = coupondate['act_coupon_date']
				first = False
		return schedules

	def validate_inputs(self, input):
		"""  do validations  """
		return True


	def calculate_next_coupon(self, coupon_date, freq, biz_day_conv,iso):
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
				raise RuntimeError('Invalid business day convention: %s' % biz_day_conv)

		return {'next_coupon_date': next_coupon_date, 'act_coupon_date': biz_day}

	def calculate_coupon_rate(self, coupon, prevCouponDate, todayDate, nextCouponDate, frequency, day_count_conv):
		days_factor = self.days_factor(prevCouponDate ,todayDate, nextCouponDate, day_count_conv,frequency)
		print days_factor
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

	def days_factor(self, prevCouponDate, todayDate,nextCouponDate,day_count_conv, frequency):
		if day_count_conv == DayCountConv.ACT_ACT:
			if todayDate == None:
				num = self.days_between(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between(todayDate,nextCouponDate)
			dem = self.days_between(prevCouponDate, nextCouponDate) * self.get_frequency_factor(frequency)
			factor = num / dem
		elif day_count_conv == DayCountConv.ACT_360:
			if todayDate == None:
				num = self.days_between(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between(todayDate,nextCouponDate)
			dem = 360 
			factor = num / dem
		elif day_count_conv == DayCountConv.ACT_365:
			if todayDate == None:
				num = self.days_between(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between(todayDate,nextCouponDate)
			dem = 365 
			factor = num / dem
		elif day_count_conv == DayCountConv.ACT_365L:
			if todayDate == None:
				num = self.days_between(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between(todayDate,nextCouponDate)
			if calendar.isleap(nextCouponDate.year):
				dem = 366
			else:
				dem = 365
			factor = num / dem
		elif day_count_conv == DayCountConv.ACT_252:
			if todayDate == None:
				num = self.days_between(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between(todayDate,nextCouponDate)
			dem = 252
			factor = num / dem

		elif day_count_conv == DayCountConv.BASIC30_360:
			if todayDate == None:
				num = self.days_between_actual(prevCouponDate,nextCouponDate)
			else:
				num = self.days_between_actual(todayDate,nextCouponDate)
			dem = 360
			factor = num / dem


		return factor


	def get_frequency_factor(self,freq):
		""" To do: Calculate Leap Year """
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
			

	def days_between(self, d1,d2):
		return (d2-d1).days * 1.0


	def days_between_actual(self, d1,d2):
		return ((d2.year -d1.year)*360 + (d2.month - d1.month)*30 + (d2.day - d1.day)) * 1.0















