app.directive('categoryList', function () {
    return {
        restrict: 'E',
        scope: {
            model: '=',
            resource: '=',
            itemsPerPage: '=?'
        },
        templateUrl: 'static/app/common/directives/category-list/category-list.template.html',
        link: function ($scope) {
            $scope.itemsPerPage = $scope.itemsPerPage || 12;
            $scope.filtering = $scope.lockedFilters || {};

            $scope.currentPage = 1;

            Object.assign($scope.filtering, {
                search: '',
                page: 1
            });

            $scope.search = function (search) {
                $scope.filtering.search = search.toLowerCase();
            };

            $scope.filter = function () {
                $scope.resource.get($scope.filtering, function (data) {
                    $scope.model = data;
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
            });
        }
    };
});
