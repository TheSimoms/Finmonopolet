app.directive('itemList', function ($q, Category, Statistics) {
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
                'category': 'Varegruppe',
                'country': 'Land',
                'producer': 'Produsent',
                'volume': 'Volum',
                'alcohol': 'Alkoholinnhold',
                'price': 'Pris',
                'litre_price': 'Pris per liter',
                'alcohol_price': 'Pris per %'
            };

            $q.all([
                Category.getAll().$promise,
                Statistics.getRanges().$promise
            ]).then(function (data) {
                $scope.filters = [
                    { title: 'Varegruppe', filter_name: 'category', data: data[0], unit: '' },
                    { title: 'Land', filter_name: 'country', unit: '' },
                    { title: 'Produsent', filter_name: 'producer', unit: '' },
                    { title: 'Passer til', filter_name: 'suits__id__in', unit: '' },
                    { title: 'Pris', filter_name: 'price__range', unit: ',-', data: data[1]['price'] },
                    { title: 'Volum', filter_name: 'volume__range', unit: ' l', data: data[1]['volume'] },
                    {
                        title: 'Alkoholinnhold', filter_name: 'alcohol__range', unit: ' %',
                        data: data[1]['alcohol']
                    },
                    {
                        title: 'Pris per liter', filter_name: 'litre_price__range', unit: 'kr per l',
                        data: data[1]['litre_price']
                    },
                    {
                        title: 'Pris per %', filter_name: 'alcohol_price__range', unit: 'kr per %',
                        data: data[1]['alcohol_price']
                    }
                ];
            });

            $scope.search = function (search) {
                $scope.filtering.search = search.toLowerCase();
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
