
;(function() {


// Declare app level module which depends on views, and components
angular.module('openFinApp', [
  'ngRoute'
]).
config(['$routeProvider', '$locationProvider', '$httpProvider', '$compileProvider' ,function($routeProvider,$locationProvider, $httpProvider, $compileProvider) {
  
  $locationProvider.html5Mode(false);

  $routeProvider
  .when('/dashboard', {
  	templateUrl: 'views/dashboard.html',
  	controller:'DashboardCtrl',
  	controllerAs: 'dashboardCtrl'
  })
  .when('/calendar', {
  	templateUrl: 'views/calendar.html',
  	controller: 'CalendarCtrl',
  	controllerAs: 'calendarCtrl'
  })
  .when('/schedule', {
  	templateUrl: 'views/schedule.html',
  	controller: 'ScheduleCtrl',
  	controllerAs: 'scheduleCtrl'
  })
  .when('/margin', {
    templateUrl: 'views/margin.html',
    controller: 'MarginCtrl',
    controllerAs: 'MarginCtrl'
  })
  .otherwise({
  	redirectTo:'/'
  });


}]);

angular
	.module('openFinApp')
	.constant('CONSTANTS',{
		'API_URL': 'http://127.0.0.1:8000'
	});

angular
	.module('openFinApp')
	.run(run);

run.$inject = ['$rootScope', '$location'];

function run($rootScope, $location) {
	console.log('Application Initialized');
}

})();


