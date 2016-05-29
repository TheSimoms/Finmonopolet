app.directive('customPagination', function () {
    return {
        restrict: 'E',
        scope: {
            model: '=',
            resource: '=',
            currentPage: '=?',
            itemsPerPage: '=?'
        },
        templateUrl: 'static/app/common/directives/pagination/pagination.template.html',
        link: function ($scope) {
            $scope.itemsPerPage = $scope.itemsPerPage || 12;

            $scope.$watch('model', function (newVal) {
                if (newVal.$resolved) {
                    $scope.totalItems = $scope.model.count;
                }
            }, true);

            if (typeof $scope.currentPage === 'undefined') {
                $scope.currentPage = 1;

                $scope.$watch('currentPage', function (newVal, oldVal) {
                    if (newVal != oldVal) {
                        $scope.resource.get({page: newVal}, function (data) {
                            $scope.model = data;
                        });
                    }
                });
            }
        }
    };
});
