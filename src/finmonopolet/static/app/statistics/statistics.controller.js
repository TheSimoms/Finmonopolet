

app.controller('StatisticsCtrl', function ($scope, Category, Country, statistics) {
    $scope.categories = Category.get();
    $scope.countries = Country.get();
});
