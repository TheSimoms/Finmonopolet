app.directive('itemList', function () {
    return {
        restrict: 'E',
        scope: {
            model: '=',
            resource: '=',
            lockedFilters: '=?',
            itemsPerPage: '=?'
        },
        templateUrl: 'static/app/common/directives/item-list/item-list.template.html',
        link: function ($scope) {
            $scope.itemsPerPage = $scope.itemsPerPage || 12;
            $scope.filtering = $scope.lockedFilters || {};

            $scope.currentPage = 1;

            $scope.ordering = {
                field: 'name',
                ascending: true
            };

            Object.assign($scope.filtering, {
                search: '',
                ordering: $scope.ordering.ascending ? '' : '-' + $scope.ordering.field,
                page: 1
            });

            $scope.orderingFields = {
                'name': 'Navn',
                'category': 'Varetype',
                'country': 'Land',
                'producer': 'Produsent',
                'volume': 'Volum',
                'alcohol': 'Alkoholinnhold',
                'price': 'Pris',
                'litre_price': 'Pris pr. liter',
                'alcohol_price': 'Pris pr. %'
            };

            $scope.search = function (search) {
                $scope.filtering.search = search;
            };

            $scope.filter = function () {
                $scope.resource.get($scope.filtering, function (data) {
                    $scope.model = data;
                });
            };

            $scope.$watch('ordering', function (newVal, oldVal) {
                if (newVal != oldVal) {
                    $scope.filtering.ordering = ($scope.ordering.ascending ? '' : '-') + $scope.ordering.field;
                }
            }, true);

            $scope.$watch('currentPage', function (newVal) {
                $scope.filtering.page = newVal;

                $scope.filter();
            });

            $scope.$watchGroup(['filtering.search', 'filtering.ordering'], function (newVal, oldVal) {
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
