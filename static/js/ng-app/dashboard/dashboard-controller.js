;(function() {
	angular
		.module('openFinApp')
		.controller('DashboardCtrl', DashboardCtrl);

	DashboardCtrl.$inject = ['$scope', '$http', '$q']

	function DashboardCtrl($scope, $http, $q) {
		$scope.message = 'Some String'
	}
})();