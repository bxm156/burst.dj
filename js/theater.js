(function(define) {
    'use strict';

    define([
        'angular',
        'angularResource',
        'jquery',
        'foundationReveal'
    ], function(angular, angularResource, $, foundationReveal) {
        angular.module('dj.burst.theater', [
            'ngResource'
        ]).factory('CurrentUserFactory', function($resource) {
            return $resource('/api/current_user');
        }).factory('RoomsFactory', function($resource) {
            return $resource('/api/room');
        }).factory('JoinFactory', function($resource) {
            return $resource('/api/room/:roomId/join');
        }).factory('QueueJoinFactory', function($resource) {
            return $resource('/api/room/:roomId/queue/join');
        }).factory('QueueLeaveFactory', function($resource) {
            return $resource('/api/room/:roomId/queue/leave');
        }).factory('ActivityFactory', function($resource) {
            return $resource('/api/room/:roomId/activity');
        }).controller('TheaterController', [
            '$scope',
            '$interval',
            'CurrentUserFactory',
            'RoomsFactory',
            'JoinFactory',
            'QueueJoinFactory',
            'QueueLeaveFactory',
            'ActivityFactory',
            function($scope, $interval, CurrentUserFactory, RoomsFactory, JoinFactory, QueueJoinFactory, QueueLeaveFactory, ActivityFactory) {
                $scope.greeting = "Deez Nuts";
                $scope.queueActionText = "Join Queue";
                $scope.isSpinning = false;

                var user = CurrentUserFactory.get({}, function() {
                    $scope.user = user;

                    // TODO: allow user to choose room
                    $scope.createRoom("Club Six");
                });

                $scope.createRoom = function(roomName) {
                    RoomsFactory.save({}, {name: roomName}, function(result) {
                        if (result.id) {
                            $scope.joinRoom(result.id);
                        }
                        else {
                            alert("Couldn't create room :-(");
                        }
                    });
                };

                $scope.listRooms = function() {
                    RoomsFactory.get(function(result) {
                        // TODO: join the room the user just created
                        $scope.rooms = result;
                    });
                };

                $scope.joinRoom = function(roomId) {
                    JoinFactory.save({roomId: roomId}, {}, function(result) {
                        if (result.id) {
                            $scope.roomId = result.id;
                            $scope.users = result.users;
                            $scope.updateUserDisplay();

                            // start the room activity loop
                            $scope.startActivityLoop();
                        }
                        else {
                            alert("Couldn't join room :-(");
                        }
                    });
                };

                $scope.startActivityLoop = function() {
                    $interval($scope.updateActivity, 2000);
                };

                $scope.toggleQueue = function() {
                    if ($scope.isSpinning) {
                        $scope.leaveQueue();
                    }
                    else {
                        $scope.joinQueue();
                    }
                };

                $scope.joinQueue = function() {
                    QueueJoinFactory.save({roomId: $scope.roomId}, {}, function(result) {
                        if (result.success) {
                            $scope.isSpinning = true;
                            // TODO: update button
                            $scope.queueActionText = "Leave Queue";
                        }
                    });
                };

                $scope.leaveQueue = function() {
                    QueueLeaveFactory.save({roomId: $scope.roomId}, {}, function(result) {
                        if (result.success) {
                            $scope.isSpinning = false;
                            $scope.queueActionText = "Join Queue";
                        }
                    });
                };

                $scope.updateUserDisplay = function() {
                    var userText = "";
                    for (var i = 0; i < $scope.users.length; i++) {
                        var user = $scope.users[i];
                        userText += user.name;
                        if (i < $scope.users.length - 1) {
                            userText += ", ";
                        }
                    }
                    $scope.usersText = userText;
                };

                $scope.updateActivity = function() {
                    ActivityFactory.get({roomId: $scope.roomId}, function(result) {

                        // TODO: change the player if current track is different
                        var currentTrack = $scope.track;
                        var latestTrack = result.track;
                        if (latestTrack) {
                            var rating = "0"
                            if (latestTrack.average_rating != undefined) {rating=latestTrack.average_rating}
                            $scope.rating_img = "o"+rating+"hstars_medium@2x.png";
                            if (!currentTrack
                                || latestTrack.id != currentTrack.id
                                || latestTrack.time_started != currentTrack.time_started) {
                                // new shit
                                $scope.track = latestTrack;
                                // TODO: offset if we're joining party late
                                player.loadVideoById({videoId: latestTrack.provider_track_id});
                            }
                            else {
                                // same shit
                            }
                        }
                        else {
                            // stop playing!
                            $scope.greeting = "Silence is golden";
                        }
                        $scope.track = result.track;

                        // TODO: change audience / queue list
                        $scope.users = result.users;
                        $scope.djs = result.djs;
                        $scope.updateUserDisplay();

                        $scope.current_dj_id = result.current_dj_id;
                    });
                };

            }
        ]);
    });
})(define);
