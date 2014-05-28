var adminApp = angular
.module('adminApp', ['ui.router'])
.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
	$urlRouterProvider.otherwise('/');
	
	$stateProvider
	.state('index', {
		url: '/',
		templateUrl: '../../static/js/templates/admin/index.html',
		controller: 'MainCtrl'
	})
	.state('users', {
		url: '/users',
		templateUrl: '../../static/js/templates/admin/users.html',
		controller: 'UserCtrl'
	})
	.state('edit_user', {
		url: '/users/:userName',
		templateUrl: '../../static/js/templates/admin/edit_user.html',
		controller: 'UserCtrl'
	});
}])
.filter('iif', function () {
   return function(input, trueValue, falseValue) {
        return input ? trueValue : falseValue;
   }
});


adminApp.service('Users', ['$http', function($http) {
	this.get = function(username) {
		var userData = $http.get('../../api1.1/users/'+username).then(function(response) {
			return response
		})
		return userData
	}
	this.all = function() {
		var userData = $http.get('../../api1.1/users/').then(function(response) {
			return response
		})
		return userData
	}
}])

adminApp.controller('UserCtrl', ['Users', '$scope', '$stateParams', '$http', function(Users, $scope, $stateParams, $http) {
	if ($stateParams.userName) {
		Users.get($stateParams.userName).then(function(response) {
			$scope.user = response.data
		})
	}
	else {
		Users.all().then(function(response) {
			$scope.limit = 5
			$scope.users = response.data.users
		})
	}
}]);