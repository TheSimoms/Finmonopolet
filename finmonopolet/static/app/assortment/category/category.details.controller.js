app.controller('CategoryDetailCtrl', function ($scope, Product, category, products) {
    $scope.category = category;
    $scope.products = products;

    $scope.productResource = Product;
});
