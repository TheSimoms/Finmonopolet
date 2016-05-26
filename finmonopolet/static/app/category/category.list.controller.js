app.controller('CategoryListCtrl', function ($scope, Category, categories) {
    $scope.categories = categories;

    $scope.pageChanged = function (currentPage) {
        Category.get({page: currentPage}, function (data) {
            $scope.categories = data;
        });
    }
});
