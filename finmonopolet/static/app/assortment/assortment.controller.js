app.controller('AssortmentCtrl', function ($scope, Category, Product, categories, products) {
    $scope.categories = categories;
    $scope.products = products;

    $scope.categoryResource = Category;
    $scope.productResource = Product;
});
