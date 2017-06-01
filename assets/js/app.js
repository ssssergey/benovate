'use strict';
var app = angular.module('app', []);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.controller('formController', function ($scope, $http) {
    $scope.clients = [];

    $http.get('/api/clients/').then(function (response) {
        $scope.clients = response.data;
    });

    $scope.submit = function () {
        $scope.result = '';
        $scope.errors_inns = '';
        $scope.errors_amount = '';
        $http({
            url: '/api/clients/' + this.client,
            method: "PUT",
            data: {'inns': this.inn, 'amount': this.amount}
        })
            .then(function successCallback(response) {
                var message = 'Операция успешно выполнена. Текущий баланс клиента ' + response.data['fullname'] +
                    ' составляет ' + response.data['account'] + ' рублей.';
                $scope.result = message;
            }, function errorCallback(response) {
                $scope.errors_inns = response.data['inns'];
                $scope.errors_amount = response.data['amount']
            });
    };

});

app.config([
    '$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
]);

