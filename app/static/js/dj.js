var djApp = angular
.module('djApp', ['ui.router', 'ui.sortable'])
.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise('/');
	
	$stateProvider
	.state('index', {
		url: '/:castNumber',
		templateUrl: '../static/js/templates/dj.html',
		controller: 'MainCtrl'
	})
}])
.filter('iif', function () {
   return function(input, trueValue, falseValue) {
        return input ? trueValue : falseValue;
   }
})
.filter('aposFix', function () {
	return function(input) {
		return input.slice(-1) == 's' ? input+'\'' : input+'\'s';
	}
})

djApp.service('Cast', ['$http', function($http) {
	this.get = function (castNumber) {
		var castData = $http.get('../api/casts/'+castNumber).then(function(response) {
			return response
		})
		return castData
	}
	this.updateOrder = function (pickOrder, castNumber) {
		var pickOrder = $http.put('../api/dj/update_order/'+castNumber, pickOrder).then(function(response) {
			return response
		})

		return pickOrder
	}
	this.updatePlayed = function (pickId) {
		var updatePlayed = $http.put('../api/dj/update_played/'+pickId).then(function(response) {
			return response
		})
		return updatePlayed
	}
}])

djApp.controller('MainCtrl', ['Cast', '$scope', '$stateParams', '$timeout', 'orderByFilter', function(Cast, $scope, $stateParams, $timeout, orderByFilter) {
	$scope.hideAll = true;
	$scope.statusMessage = 'Drag and drop to rearrange';
	$scope.loadData = function() {
		Cast.get($stateParams.castNumber).then(function(response) {
			$scope.castData = response.data;
			$scope.castData.picks = orderByFilter(response.data.picks, ['dj_list_position']);
		})
	}
	$scope.loadData();

	$scope.sortableOptions = {
		start: function(e, ui) {
			console.log('here we go');
		},
		sort: function(e, ui) {
			$scope.statusMessage = 'Change to position '+(ui.placeholder.index()+1);
			$scope.$apply();
		},
		stop: function(e, ui) {
			console.log('we have arrived');
			var pickOrder = $scope.castData.picks.map(function(x) {
				return {
					id: x.id,
					position: $scope.castData.picks.indexOf(x)
				}
			})
			Cast.updateOrder(pickOrder, $stateParams.castNumber).then(function(response) {
				if (response.data.slice(0, 4) == 'Must') {
					$scope.castData.picks = orderByFilter($scope.castData.picks, ['dj_list_position']);
				}
				$scope.statusMessage = response.data;
			})
			$scope.loadData()
		},
		opacity: '0.5',
		tolerance: 'pointer',
		connectWith: '.list-picks',
		helper: 'clone',
		appendTo: 'body',
		zIndex: 9999
	}
}])
djApp.directive('toggleall', function() {
	return {
		restrict: 'E',
		transclude: true,
		template: '<button ng-transclude ng-click=\'toggleAll()\'></button>',
		link: function(scope, element, attrs) {
			scope.toggleAll = function() {
				scope.hideAll == true ? angular.element('div.description').show() : angular.element('div.description').hide();
				angular.element('i.fa').toggleClass('fa-chevron-circle-up fa-chevron-circle-down');
				scope.hideAll = !scope.hideAll;
			}
		}
	}
})
djApp.directive('toggleplayed', ['Cast', '$timeout', function(Cast, $timeout) {
	return {
		restrict: 'E',
		template: '<input class="pull-right" type="checkbox" ng-click="togglePlayed($event)" ng-model="pick.played" />',
		link: function(scope, element, attrs) {
			scope.togglePlayed = function($event) {
				Cast.updatePlayed(scope.pick.id).then(function(response) {
					if (response.data.slice(0,4) == 'Must') {
						scope.pick.played = !scope.pick.played;
					}
					angular.element('small.statusMessage').scope().statusMessage = response.data;
				})
			}
		}
	}
}])
djApp.directive('pick', function() {
	return {
		restrict: 'E',
		templateUrl: '../static/js/templates/pick.html',
		link: function(scope, element, attrs) {
			angular.element('div.description').hide();
			scope.toggleDescription = function(className) {
				element.find('div.description').toggle();
				element.find('i.fa').toggleClass('fa-chevron-circle-up fa-chevron-circle-down');
			}
		}
	}
})