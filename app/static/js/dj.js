var djApp = angular.module('djApp', ['ngRoute', 'ui.sortable']);

djApp.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl: '../static/js/templates/dj.html',
				controller: 'sortableController'
			})
			.otherwise({
				redirectTo: '/'
			});
	}
]);

djApp.controller('sortableController', ['$scope', '$http', '$routeParams', 
function ($scope, $http, $routeParams) {
	var apiUrl = 'http://localhost:5000/api/casts/' + $routeParams.cast;
	$http.get(apiUrl).success(function(data) {
		$scope.picks = data.picks;

	});

	$scope.sortableOptions = {
		update: function(e, ui) {
			ui.item.startPos = ui.item.index();
		},
		stop: function(e, ui) {
			$scope.positionData = 
			'Cast ' + $routeParams.cast + 
			' Pick ' + ui.item.context.id + 
			' Start pos ' + ui.item.startPos + 
			' End pos ' + ui.item.index();
		}
	};
}]);