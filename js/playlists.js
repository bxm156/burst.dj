(function(define) {
    'use strict';

    define([
        'angular',
        'angularResource',
        'jquery',
    ], function(angular, angularResource, $) {
        angular.module('dj.burst.playlists', [
            'ngResource'
        ]).factory('CurrentUserFactory', function($resource) {
            return $resource('/api/current_user');
        }).factory('PlaylistFactory', function($resource) {
            return $resource('/api/user/:userId/playlist/:id', {
                    userId: '@userId',
                    id: '@id',
            });
        }).factory('MusicSearchFactory', function($resource) {
            return $resource('/api/music_search/:query');
        }).controller('PlaylistController', [
            '$scope',
            'CurrentUserFactory',
            'PlaylistFactory',
            'MusicSearchFactory',
            function($scope, CurrentUserFactory, PlaylistFactory, MusicSearchFactory) {
                var user = CurrentUserFactory.get({}, function() {
                    $scope.user = user;
                    $scope.greeting = user.name + "'s playlists";
                    $scope.playlists = PlaylistFactory.get({userId:user.id});
                });
                $scope.create = function(playlist) {
                    $('#createPlaylist').foundation('reveal','open');
                };
                $scope.edit = function(playlist) {
                    //
                };
                $scope.search = function(query) {
                    MusicSearchFactory.get({query: query.term}, function(result) {
                        alert(results);
                    });
                };
            }
        ]);
    });
})(define);
