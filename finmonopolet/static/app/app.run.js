app.run(
    function($rootScope) {
        $rootScope.$on('$stateChangeStart', function (event, current) {
            $rootScope.title = 'Finmonopolet' + (current.title.length ? ' - ' + current.title : '');
        });
    }
);
