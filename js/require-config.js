'use strict';

require.config({
    baseUrl: '/static',
    paths: {
        angular: 'angular/angular',
        angularResource: 'angular-resource/angular-resource',
        app: 'js/app',
        jquery: 'jquery/dist/jquery',
        jqueryBridget: 'jquery-bridget/jquery.bridget',
        foundation: 'foundation/js/foundation',
        foundationReveal: 'foundation/js/foundation/foundation.reveal',
        underscore: 'underscore/underscore'
    },
    shim: {
        'angular': {'exports': 'angular'},
        'angularResource': {
            deps: ['angular']
        },
        'foundation': {
            deps: ['jquery']
        },
        'foundationReveal': {
            deps: ['foundation']
        },
    },
    priority: [
        'angular'
    ]
});

require([
    'jquery',
    'jqueryBridget'
    ], function($, bridget) {
    }
);
