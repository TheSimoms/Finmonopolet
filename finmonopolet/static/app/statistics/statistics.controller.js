app.controller('StatisticsCtrl', function ($scope, category, statistics) {
    $scope.category = category;
    $scope.title = 'Statistikk';

    $scope.statistics = {
        'numeric': {}
    };

    if ($scope.category != null) {
        $scope.category.$promise.then(function (data) {
            $scope.title = $scope.title + ' - ' + data.name;
        });
    }

    statistics.$promise.then(function (data) {
        console.log(data);
    });
});
