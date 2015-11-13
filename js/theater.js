(function(define) {
    'use strict';

    define([
        'angular',
    ], function(angular) {
        angular.module('dj.burst.theater', [    
        ]).controller('TheaterController', ['$scope', function($scope) {
            $scope.greeting = "Movie";       
        }]);
    });
})(define);
