;(function() {
	angular
		.module('openFinApp')
		.controller('CalendarCtrl', CalendarCtrl);


	CalendarCtrl.$inject = ['$scope', '$http']

	function CalendarCtrl($scope, $http) {

		$scope.loadHoliday = function () {
			$scope.holidays = [{ date: '2015-01-01', name: 'New Year'}, { date: '2015-12-25', name: 'Christmas'}];
		};

		$scope.getHoliday = function () {


			var calendar_url = '/country/'+$scope.iso+ '/' + $scope.year;

			$http({
				method: 'GET',
				url: calendar_url,
				params:null,
				data:null
			}).then(function(data){
				$scope.holidays = data.data
			}, function(error){
				$scope.holidays = [{ date: 'Server Error!', name: ''}];
			});
			
		}

	}
})();