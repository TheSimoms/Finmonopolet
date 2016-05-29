app.controller('CategoryDetailCtrl', function ($scope, $state, Product, category, products) {
    $scope.category = category;
    $scope.products = products;

    $scope.productResource = Product;

    $scope.lockedFilters = {
        category: $state.params.categoryId
    };
});
