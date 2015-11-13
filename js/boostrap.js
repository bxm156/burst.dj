require([
    'angular',
    'underscore',
    'app',
    ], function (angular, _, app) {
        var $body = angular.element(document.getElementsByTagName('body')[0]);
        angular.element().ready(function() {
            angular.bootstrap(document, ['dj.burst']);
        });
    }
);
