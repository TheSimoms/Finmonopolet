app.controller('StoreDetailsCtrl', function ($scope, store, uiGmapGoogleMapApi) {
    $scope.store = store;

    $scope.store.$promise.then(function () {
        uiGmapGoogleMapApi.then(function () {
            $scope.marker = { latitude: $scope.store.latitude, longitude: $scope.store.longitude };
            $scope.map = { center: $scope.marker, zoom: 14 };
        });
    });
});
