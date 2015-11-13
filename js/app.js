(function(define) {
    'use strict';

    define([
        'angular',
    ], function(angular) {
        angular.module('dj.burst', [
        ]).config(['$compileProvider', function($compileProvider) {
            $compileProvider.debugInfoEnabled(true);
            alert("Hello World");
        }]);
    });
})(define);
