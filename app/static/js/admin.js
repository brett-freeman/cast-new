var adminApp = angular
.module('adminApp', ['ui.router'])
.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise('/');
	
	$stateProvider
	.state('index', {
		url: '/',
		templateUrl: '../../static/js/templates/admin/index.html',
		controller: 'MainCtrl'
	});
}])
.filter('iif', function () {
   return function(input, trueValue, falseValue) {
        return input ? trueValue : falseValue;
   }
});


adminApp.service('Users', ['$http', function($http) {
	this.get = function (username) {
		var userData = $http.get('../../api/users/'+username).then(function(response) {
			return response
		})
		return userData
	}
	this.all = function() {
		var userData = $http.get('../../api/users/').then(function(response) {
			return response
		})
		return userData
	}
}])

adminApp.controller('MainCtrl', ['Users', '$scope', '$stateParams', '$http', function(Users, $scope, $stateParams, $http) {
	Users.get('admin').then(function(response) {
		$scope.username = response.data.username
	})
	Users.all().then(function(response) {
		$scope.users = response.data.users
		console.log($scope.users[0])
	})
}]);