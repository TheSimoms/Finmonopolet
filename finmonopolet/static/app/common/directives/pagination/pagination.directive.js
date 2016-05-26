app.directive('customPagination', function () {
    return {
        restrict: 'E',
        scope: {
            totalItems: '=',
            pageChanged: '=',
            itemsPerPage: '=?'
        },
        templateUrl: 'static/app/common/directives/pagination/pagination.template.html',
        link: function ($scope) {
            $scope.itemsPerPage = $scope.itemsPerPage || 6;
        }
    };
});
