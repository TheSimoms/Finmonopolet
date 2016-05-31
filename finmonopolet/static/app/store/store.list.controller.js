app.controller('StoreListCtrl', function ($scope, Store, stores, storeLocations, uiGmapGoogleMapApi) {
    $scope.stores = stores;
    $scope.storeLocations = storeLocations;

    $scope.storeResource = Store;

    $scope.currentPage = 1;

    $scope.filtering = {
        search: '',
        page: 1
    };

    $scope.currentDay = new Date().getDay();

    var weekdays = [
        'sunday',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday'
    ];

    $scope.getOpeningTimes = function (openingTimesDict, weekday) {
        var openingTimes = openingTimesDict[weekdays[weekday]];

        if (!openingTimes) {
            return 'Stengt';
        }

        return openingTimes;
    };

    $scope.search = function (search) {
        $scope.filtering.search = search;
    };

    $scope.filter = function () {
        Store.get($scope.filtering, function (data) {
            $scope.stores = data;
        });
    };

    $scope.$watch('currentPage', function (newVal) {
        $scope.filtering.page = newVal;

        $scope.filter();
    });

    $scope.$watch('filtering.search', function (newVal, oldVal) {
        if (newVal != oldVal) {
            if ($scope.currentPage == 1) {
                $scope.filter();
            } else {
                $scope.currentPage = 1;
            }
        }
    }, true);

    $scope.storeLocations.$promise.then(function () {
        uiGmapGoogleMapApi.then(function () {
            $scope.center = {
                latitude: '65.556772',
                longitude: '18.0048495'
            };

            $scope.markers = [];

            for (var i = 0; i < $scope.storeLocations.length; i++) {
                var store = $scope.storeLocations[i];

                $scope.markers.push({
                    id: store.id,
                    position: {
                        latitude: store.latitude,
                        longitude: store.longitude
                    },
                    options: {
                        title: store.name
                    }
                });
            }

            $scope.map = {
                center: $scope.center,
                zoom: 4
            };
        });
    });
});
