;(function() {
	angular
		.module('openFinApp')
		.controller('ScheduleCtrl', ScheduleCtrl);


	ScheduleCtrl.$inject = ['$scope', '$http']

	function ScheduleCtrl($scope, $http) {

		$scope.loadSchedule = function () {
			$scope.schedule = [{  "securityId": "A12345",
    "nextCouponDate": "2016-11-25",
    "maturityDate": "2017-03-10",
    "frequency": "1_M",
    "businessDayConvention": "ADJMBC",
    "dayCountConvention": "30/Actual",
    "coupon": 1.24}];
		};

		$scope.getSchedule = function () {
			/*
			var input = {
				JSON.stringify({
					securityId: $scope.securityId,
					nextCouponDate: $scope.nextCouponDate,
					maturityDate: $scope.maturityDate,
					frequency: $scope.frequency,
					businessDayConvention: $scope.businessDayConvention,
					dayCountBasis: $scope.dayCountBasis,
					coupon: $scope.coupon
				})
			}; */

			var loaddata = {"securityId": $scope.securityId,
    						"nextCouponDate": $scope.nextCouponDate,
    						"prevCouponDate": $scope.prevCouponDate,
    						"maturityDate": $scope.maturityDate,
    						"iso": $scope.iso,
    						"frequency": $scope.frequency,
    						"businessDayConvention": $scope.businessDayConvention,
    						"dayCountConvention": $scope.dayCountBasis,
    						"coupon": $scope.coupon}

			var schedule_url =  '/cschedule';

			$http({
				method: 'POST',
				url: schedule_url,
				params:null,
				data: loaddata
			}).then(function(data){
				$scope.schedule = data.data
			}, function(error){
				$scope.schedule = [{ date: 'Server Error!', name: ''}];
			});
			
		}

	}
})();