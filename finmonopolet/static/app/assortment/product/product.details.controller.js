app.controller('ProductDetailCtrl', function ($scope, product) {
    $scope.product = product;

    $scope.product.$promise.then(function () {
        $scope.category = $scope.product.category;
    });
});
