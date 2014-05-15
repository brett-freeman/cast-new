var djApp = angular
.module('djApp', ['ui.router', 'ui.sortable'])
.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise('/');
	
	$stateProvider
	.state('index', {
		url: '/:castId',
		templateUrl: '../static/js/templates/dj.html',
		controller: 'sortableCtrl'
	})
}]);

djApp.controller('sortableCtrl', ['$scope', '$http', 'orderByFilter', '$stateParams', function($scope, $http, orderByFilter, $stateParams) {
	$http.get('../api/casts/' + $stateParams.castId).success(function(data) {
		$scope.picks = orderByFilter(data.picks, ['dj_list_position']);
	});
	$scope.sortableOptions = {
		stop: function(e, ui) {
			var pick_order = $scope.picks.map(function(i) {
				return { 
					id: i.id, 
					position: $scope.picks.indexOf(i) 
				};
			});
			$http.put('../api/dj/update_order/' + $stateParams.castId, pick_order).success(function(data) {
				console.log(data);
				$scope.picks = orderByFilter(data.picks, ['dj_list_position']);
			});
		}
	};
}]);