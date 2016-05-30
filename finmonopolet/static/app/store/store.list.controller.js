app.controller('StoreListCtrl', function ($scope, Store, stores, uiGmapGoogleMapApi) {
    $scope.stores = stores;

    $scope.stores.$promise.then(function () {
        uiGmapGoogleMapApi.then(function () {
            $scope.markers = [];
            $scope.center = {
                latitude: '65.556772',
                longitude: '18.0048495'
            };

            for (var i = 0; i < $scope.stores.length; i++) {
                var store = $scope.stores[i];

                $scope.markers.push({
                    id: i,
                    latitude: store.latitude,
                    longitude: store.longitude
                });
            }

            $scope.map = { center: $scope.center, zoom: 4 };
        });
    });
});
