app.directive('customPagination', function () {
    return {
        restrict: 'E',
        scope: {
            model: '=',
            resource: '=',
            itemsPerPage: '=?'
        },
        templateUrl: 'static/app/common/directives/pagination/pagination.template.html',
        link: function ($scope) {
            $scope.itemsPerPage = $scope.itemsPerPage || 12;
            $scope.model.$promise.then(function () {
                $scope.totalItems = $scope.model.count;
            });

            $scope.pageChanged = function (currentPage) {
                $scope.resource.get({page: currentPage}, function (data) {
                    $scope.model = data;
                });
            };
        }
    };
});
