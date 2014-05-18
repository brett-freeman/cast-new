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
}]).
filter('iif', function () {
   return function(input, trueValue, falseValue) {
        return input ? trueValue : falseValue;
   };
});

djApp.controller('sortableCtrl', ['$scope', '$http', 'orderByFilter', '$stateParams', '$timeout', function($scope, $http, orderByFilter, $stateParams, $timeout) {
	$http.get('../api/casts/' + $stateParams.castId).success(function(data) {
		$scope.castNumber = $stateParams.castId;
		$scope.picks = orderByFilter(data.picks, ['dj_list_position']);
	});
	$scope.sortableOptions = {
		start: function(e, ui) {
			$scope.saveStatus = '';
			$scope.hideAll = true;
		},
		stop: function(e, ui) {
			$scope.hideAll = false;
			var pick_order = $scope.picks.map(function(i) {
				return { 
					id: i.id, 
					position: $scope.picks.indexOf(i) 
				};
			});
			$http.put('../api/dj/update_order/' + $stateParams.castId, pick_order).success(function(data) {
				$scope.saveStatus = data;
				if (data.slice(0, 4) == 'Must') {
					$scope.picks = orderByFilter($scope.picks, ['dj_list_position']);
				}
			});
			$timeout(function() {
				$scope.saveStatus = '';
			}, 2000);
		},
		change: function(e, ui) {
			position = ui.placeholder.index()
			$scope.saveStatus = 'Change to position '+position;
			$scope.$apply();
		},
		opacity: '0.5',
		tolerance: 'pointer',
		connectWith: '.list-picks',
		cursor: 'move',
		helper: 'clone',
		appendTo: 'body',
		zIndex: 9999

	};
	$scope.togglePlayed = function($event, pickId) {
		$http.put('../api/dj/update_played/'+pickId)
		.success(function(data) {
			$scope.saveStatus = data;
			if (data.slice(0,4) == 'Must') {
				$event.target.checked = !$event.target.checked;
			}
			$timeout(function() {
				$scope.saveStatus = '';
			}, 2000);
		});
	};
}]);