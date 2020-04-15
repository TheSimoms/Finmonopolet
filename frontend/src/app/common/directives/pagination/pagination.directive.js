app.directive('customPagination', function () {
    return {
        restrict: 'E',
        scope: {
            model: '=',
            resource: '=',
            currentPage: '=?',
            itemsPerPage: '=?',
            numberOfPages: '=?',
            showBoundaries: '=?'
        },
        templateUrl: '/app/common/directives/pagination/pagination.template.html',
        link: function ($scope) {
            $scope.itemsPerPage = $scope.itemsPerPage || 12;
            $scope.numberOfPages = $scope.numberOfPages || 10;

            $scope.$watch('model', (newVal) => {
                if (typeof newVal !== 'undefined' && newVal.$resolved) {
                    $scope.totalItems = $scope.model.count;
                }
            }, true);

            if (typeof $scope.currentPage === 'undefined') {
                $scope.currentPage = 1;

                var filterCounter = 0;

                $scope.$watch('currentPage', (newVal) => {
                    filterCounter = (filterCounter + 1) % 100;

                    var currentCounter = filterCounter;

                    $scope.resource.get({page: newVal}, (data) => {
                        if (currentCounter === filterCounter) {
                            $scope.model = data;
                        }
                    });
                });
            }
        }
    };
});
