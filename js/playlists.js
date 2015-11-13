(function(define) {
    'use strict';

    define([
        'angular',
        'angularResource',
        'jquery',
        'foundationReveal'
    ], function(angular, angularResource, $, foundationReveal) {
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
                    $scope.playlists = PlaylistFactory.query({userId:user.id});
                });
                $scope.create = function(playlist) {
                    $('#createPlaylist').foundation('reveal','open');
                };
                $scope.edit = function(playlist) {
                    //
                };
                $scope.search = function(query) {
                    MusicSearchFactory.get({query: query.term}, function(result) {
                        var results = [];
                        for (var i = 0; i < result.items.length; i++){
                            if (result.items[i].id.videoId){
                                var thingy = {
                                    thumbnail_url: result.items[i].snippet.thumbnails.default.url,
                                    title: result.items[i].snippet.title,
                                    video_id: result.items[i].id.videoId
                                }
                                results.push(thingy);
                            }
                         }
                        $scope.search_results = results;
                    });
                };

            }
        ]);
    });
})(define);
