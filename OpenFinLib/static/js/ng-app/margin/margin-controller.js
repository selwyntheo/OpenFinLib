;(function() {
	angular
		.module('openFinApp')
		.controller('MarginCtrl', MarginCtrl);


	MarginCtrl.$inject = ['$scope', '$http']

	function MarginCtrl($scope, $http) {

		$scope.loadPAI = function () {
			$scope.holidays = [{ date: '2015-01-01', name: 'New Year'}, { date: '2015-12-25', name: 'Christmas'}];
		};

		$scope.getPAI = function () {


			var margin_url = '/margin/'+$scope.CCP+ '/' + $scope.currency;

			$http({
				method: 'GET',
				url: margin_url,
				params:null,
				data:null
			}).then(function(data){
				$scope.pai = data.data
			}, function(error){
				$scope.pai = [{ date: 'Server Error!', name: ''}];
			});
			
		}

	}
})();