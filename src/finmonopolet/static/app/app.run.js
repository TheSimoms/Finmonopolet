app.run(function ($rootScope, $state) {
    $rootScope.isActiveState = function (state) {
        return $state.current.name.startsWith(state);
    };
});
