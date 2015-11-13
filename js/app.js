(function(define) {
    'use strict';

    define([
        'angular',
        'js/playlists',
        'js/theater'
    ], function(angular) {
        angular.module('dj.burst', [
            'dj.burst.playlists',
            'dj.burst.theater'
        ]).config(['$compileProvider', function($compileProvider) {
            $compileProvider.debugInfoEnabled(true);
        }]);
    });
})(define);
