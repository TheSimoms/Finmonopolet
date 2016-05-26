app.controller('CategoryDetailCtrl', function ($scope, Product, category, products) {
    $scope.category = category;
    $scope.products = products;

    $scope.filtering = {
        search: '',
        ordering: ''
    };

    $scope.pageChanged = function (currentPage) {
        Product.get(
            {
                category: category.id,
                page: currentPage,
                ordering: $scope.filtering.ordering
            },
            function (data) {
                $scope.products = data;
            }
        );
    }
});
