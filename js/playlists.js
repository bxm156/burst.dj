(function(define) {
    'use strict';

    define([
        'angular',
        'angularResource',
    ], function(angular, angularResource) {
        angular.module('dj.burst.playlists', [
            'ngResource'
        ]).factory('CurrentUserFactory', function($resource) {
            return $resource('/api/current_user');
        }).factory('PlaylistFactory', function($resource) {
            return $resource('/api/user/:userId/playlist/:id', {
                    userId: '@userId',
                    id: '@id',
            });
        }).controller('PlaylistController', [
            '$scope',
            'CurrentUserFactory',
            'PlaylistFactory',
            function($scope, CurrentUserFactory, PlaylistFactory) {
                var user = CurrentUserFactory.get({}, function() {
                    $scope.user = user;
                    $scope.greeting = user.name + "'s playlists";
                });
                PlaylistFactory.get({userId:1, id:2});
            }
        ]);
    });
})(define);
