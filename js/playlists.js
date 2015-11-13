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
        }).factory('TrackFactory', function($resource) {
            return $resource('/api/user/:userId/playlist/:playlistId/add_track');
        }).factory('MusicSearchFactory', function($resource) {
            return $resource('/api/music_search/:query');
        }).factory('ActivePlaylistFactory', function($resource) {
            return $resource('/api/user/:userId/active_playlist');
        }).factory('ListPlaylistTrackFactory', function($resource) {
            return $resource('/api/user/:userId/playlist/:playlistId');
        }).controller('PlaylistController', [
            '$scope',
            'CurrentUserFactory',
            'PlaylistFactory',
            'ActivePlaylistFactory',
            'TrackFactory',
            'MusicSearchFactory',
            'ListPlaylistTrackFactory',
            function($scope, CurrentUserFactory, PlaylistFactory, ActivePlaylistFactory, TrackFactory, MusicSearchFactory, ListPlaylistTrackFactory) {
                var user = CurrentUserFactory.get({}, function() {
                    $scope.user = user;
                    $scope.greeting = user.name + "'s playlists";
                    $scope.playlists = PlaylistFactory.query({userId:user.id});
                    ActivePlaylistFactory.get({
                        userId: $scope.user.id,
                    },  function($playlist) {
                        $scope.active_playlist = $playlist  
                    });
                });
                $scope.create = function($playlist) {
                    PlaylistFactory.save({
                        userId: $scope.user.id,
                        name: $playlist.name,
                    }, function($playlist) {
                        $scope.createPlaylistTitle = "New Playlist: " + $playlist.name;
                        $scope.new_playlist = $playlist;
                        $('#createPlaylist').foundation('reveal','open');
                        PlaylistFactory.query({userId:user.id}, function($playlists) {
                            $scope.playlists = $playlists;
                        });
                    });
                };
                $scope.edit = function($playlist) {
                    ListPlaylistTrackFactory.get({
                        userId: $scope.user.id,
                        playlistId: $playlist.id
                    }, function(result) {
                        $scope.showPlaylist = result
                        $scope.playlistTitle = $playlist.name

                        var tracks = []
                        for (var i = 0; i < result.tracks.length; i++){
                            tracks.push(result.tracks[i]);
                        }
                        $scope.playlistTracks = tracks
                        $('#playlistTracks').foundation('reveal','open');
                    });
                };
                $scope.activate = function($playlist) {
                    ActivePlaylistFactory.save({
                        userId: $scope.user.id,
                    }, {
                        playlist_id: $playlist.id
                    }, function($playlist) {
                        $scope.active_playlist = $playlist  
                    });
                };
                $scope.addToPlaylist = function($event, $playlist, $video_id) {
                    TrackFactory.save({
                        userId: $scope.user.id,
                        playlistId: $playlist.id
                    }, {
                        provider_track_id: $video_id,
                        provider: 'youtube',
                    });
                    $event.target.setAttribute('class', 'disabled-result');
                };
                $scope.search = function($query) {
                    MusicSearchFactory.get({query: $query.term}, function(result) {
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
