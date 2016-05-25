app.run(['$rootScope', function($rootScope) {
    $rootScope.$on('$routeChangeSuccess', function (event, current) {
        var title = current.$$route.title;

        $rootScope.title = 'Finmonopolet' + (title.length ? ' - ' + title : '');
    });
}]);
