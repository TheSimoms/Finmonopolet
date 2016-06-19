app.directive('customPagination', function () {
    return {
        restrict: 'E',
        scope: {
            model: '=',
            resource: '=',
            currentPage: '=?',
            itemsPerPage: '=?',
            numberOfPages: '=?',
            labels: '=?',
            showBoundaries: '=?'
        },
        templateUrl: 'static/app/common/directives/pagination/pagination.template.html',
        link: function ($scope) {
            $scope.itemsPerPage = $scope.itemsPerPage || 12;
            $scope.numberOfPages = $scope.numberOfPages || 20;

            $scope.$watch('model', function (newVal) {
                if (typeof newVal !== 'undefined' && newVal.$resolved) {
                    $scope.totalItems = $scope.model.count;
                }
            }, true);

            $scope.labels = {
                first: '«',
                previous: '‹',
                next: '›',
                last: '»'
            } || $scope.labels;

            if (typeof $scope.currentPage === 'undefined') {
                $scope.currentPage = 1;

                var filterCounter = 0;

                $scope.$watch('currentPage', function (newVal) {
                    filterCounter = (filterCounter + 1) % 100;

                    var currentCounter = filterCounter;

                    $scope.resource.get({page: newVal}, function (data) {
                        if (currentCounter === filterCounter) {
                            $scope.model = data;
                        }
                    });
                });
            }
        }
    };
});
