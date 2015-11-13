(function(define) {
    'use strict';

    define([
        'angular',
        'angularResource',
    ], function(angular, angularResource) {
        angular.module('dj.burst.playlists', [
            'ngResource'
        ]).factory('PlaylistFactory', function($resource) {
            return $resource('/user/:userId/playlist/:id', {
                    userId: '@userId',
                    id: '@id',
            });
        }).controller('PlaylistController', ['$scope', 'PlaylistFactory', function($scope, PlaylistFactory) {
            $scope.greeting = "Hello";
            PlaylistFactory.get({userId:1, id:2});
        }]);
    });
})(define);
