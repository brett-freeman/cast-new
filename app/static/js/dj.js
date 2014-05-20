var djApp = angular
.module('djApp', ['ui.router', 'ui.sortable', 'doowb.angular-pusher', 'ngSanitize'])
.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise('/');
	
	$stateProvider
	.state('index', {
		url: '/:castId',
		templateUrl: '../static/js/templates/dj.html',
		controller: 'sortableCtrl'
	})
}])
.filter('iif', function () {
   return function(input, trueValue, falseValue) {
        return input ? trueValue : falseValue;
   };
});

djApp.controller('sortableCtrl', ['$scope', '$http', 'orderByFilter', '$stateParams', '$timeout', 'Pusher', function($scope, $http, orderByFilter, $stateParams, $timeout, Pusher) {
	$scope.listView = false;
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
		forceHelperSize: true,
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


djApp.directive('toggledesc', function() {
	return {
		restrict: 'A',
		scope: {},
		link: function(scope, element) {
			element.bind('click', function () {
				if (scope.hide == true) {
					scope.$apply(scope.hide = false);
					element.next().addClass('hidden');
					element.next().next().addClass('hidden');
				}
				else {
					scope.$apply(scope.hide = true);
					element.next().removeClass('hidden');
					element.next().next().removeClass('hidden');
				}
			})
		}
	}
});

djApp.directive('pickheader', function() {
	return {
		restrict: 'E',
		link: function(scope, element, attrs) {
			if (scope.pick.username.slice(-1) == 's') {
				element.html(scope.pick.username+'\' pick');
			} 
			else {
				element.html(scope.pick.username+'\'s pick');
			}
		}
	}
});

djApp.directive('toggleview', ['$document', '$sce', function($document, $sce) {
	return {
		restrict: 'A',
		link: function(scope, element, attrs) {
			element.bind('click', function() {
				scope.$apply(scope.listView = !scope.listView);
				if (scope.listView == true) {
					element.html('Grid');
					element.parent().find('li.list-picks').removeClass('col-md-3 col-lg-3');
					element.parent().find('div.desc').removeClass('col-md-11 col-lg-11');
					element.parent().find('div.desc')
					.css({'position': 'relative',
						  'color': '#fff',
						  'width': '100%',
						  'padding-bottom': '10px'
					});
					element.parent().find('span.desc').css('visibility', 'hidden');
				}
				else {
					scope.listViewBreaks = '';
					element.html('List');
					element.parent().find('li.list-picks').addClass('col-md-3 col-lg-3');
					element.parent().find('div.desc').addClass('col-md-11 col-lg-11');
					element.parent().find('div.desc')
					.css({'position': 'absolute',
						  'color': '#fff',
						  'width': '100%'
					});
					element.parent().find('span.desc')
						.css({'visibility:': 'show'
					});
				}
			})
		}
	}
}]);

djApp.directive('nowplaying', function() {
	return {
		restrict: 'E',
		scope: {
			picks: '='
		},
		link: function(scope, element, attrs) {
			console.log(scope['picks']);
		}
	}
});