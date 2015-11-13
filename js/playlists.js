(function(define) {
    'use strict';

    define([
        'angular',
    ], function(angular) {
        angular.module('dj.burst.playlists', [    
        ]).controller('PlaylistController', ['$scope', function($scope) {
            $scope.greeting = "Hello";       
        }]);
    });
})(define);
