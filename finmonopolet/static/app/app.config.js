app.config(['$locationProvider',
    function config($locationProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
    }
]);

app.config(['$routeProvider',
    function config($routeProvider) {
        $routeProvider
            .when('/', {
                title: ''
            })
            .otherwise({
                redirectTo:'/'
            });
    }
]);
