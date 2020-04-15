var app = angular.module('finmonopolet',
    [
        'ngAnimate',
        'ngResource',
        'ngTouch',

        'ui.bootstrap',
        'ui.router',

        'ncy-angular-breadcrumb',

        'smart-table',
        'angularMoment',
    ]
);

app.constant('API_HOST', 'http://localhost:8081');
