app.directive('itemList', function ($q, $timeout, Product, Category, Country, Producer, Suits) {
    return {
        restrict: 'E',
        scope: {
            title: '=?',
            lockedFilters: '=?',
            itemsPerPage: '=?'
        },
        templateUrl: 'static/app/common/directives/item-list/item-list.template.html',
        link: function ($scope) {
            $scope.resource = Product;

            $scope.filtering = $scope.lockedFilters || {};

            $scope.itemsPerPage = $scope.itemsPerPage || 12;
            $scope.currentPage = 1;

            $scope.ordering = {
                field: 'canonical_name',
                ascending: true
            };

            Object.assign($scope.filtering, {
                search: '',
                ordering: $scope.ordering.ascending ? '' : '-' + $scope.ordering.field,
                page: 1
            });

            $scope.model = $scope.resource.get($scope.filtering);

            $scope.orderingFields = {
                'canonical_name': 'Navn',
                'category': 'Varegruppe',
                'country': 'Land',
                'producer': 'Produsent',
                'volume': 'Volum',
                'alcohol': 'Alkoholinnhold',
                'price': 'Pris',
                'litre_price': 'Pris pr. liter',
                'alcohol_price': 'Pris pr. %'
            };

            $scope.filters = {
                category: {
                    title: 'Varegruppe', filter_name: 'category', resource: Category, data: [], selected: []
                },
                country: {
                    title: 'Land', filter_name: 'country', resource: Country, data: [], selected: []
                },
                producer: {
                    title: 'Produsent', filter_name: 'producer', resource: Producer, data: [], selected: []
                },
                suits: {
                    title: 'Passer til', filter_name: 'suits', resource: Suits, data: [], selected: []
                }
            };

            $scope.rangeFilters = {
                price: {
                    title: 'Pris', unit: ',-', pristine: true,
                    type: 'range', values: ['', '']
                },
                volume: {
                    title: 'Volum',  unit: ' l', pristine: true,
                    type: 'range', values: ['', '']
                },
                alcohol: {
                    title: 'Alkoholinnhold',  unit: ' %', pristine: true,
                    type: 'range', values: ['', '']
                },
                litre_price: {
                    title: 'Pris pr. liter',  unit: ',- pr. l', pristine: true,
                    type: 'range', values: ['', '']
                },
                alcohol_price: {
                    title: 'Pris pr. %',  unit: ',- pr. %', pristine: true,
                    type: 'range', values: ['', '']
                }
            };

            $scope.search = function (search) {
                $scope.filtering.search = search.toLowerCase();
            };

            $scope.updateListFilter = function (filter, item) {
                var index = filter.selected.indexOf(item);

                if (index >= 0) {
                    filter.selected.splice(index, 1);
                } else {
                    filter.selected.push(item);
                }

                if (filter.selected.length == 0) {
                    delete $scope.filtering[filter.filter_name];
                } else {
                    $scope.filtering[filter.filter_name] = filter.selected.map(function (item) {
                        return item.id;
                    }).join();
                }
            };

            $scope.isRangeFilterActive = function (filter) {
                for (var i = 0; i < 2; i++) {
                    if (filter.values[i] != '') {
                        return true;
                    }
                }

                return false;
            };

            $scope.getFilterString = function (filter) {
                var filterValues = [parseFloat(filter.values[0]), parseFloat(filter.values[1])];

                if (isNaN(filterValues[0]) && !isNaN(filterValues[1])) {
                    return 'Under ' +  filterValues[1];
                } else if (isNaN(filterValues[1]) && !isNaN(filterValues[0])) {
                    return 'Over ' + filterValues[0];
                } else if (!isNaN(filterValues[0]) && !isNaN(filterValues[1])) {
                    if (filterValues[0] <= filterValues[1]) {
                        return filterValues[0] + ' - ' + filterValues[1];
                    }
                }
            };

            $scope.updateRangeFilter = function (filter, filterLabel) {
                var queryString = filterLabel + '__';
                var queryValue;

                var filterValues = [parseFloat(filter.values[0]), parseFloat(filter.values[1])];

                if (isNaN(filterValues[0]) && !isNaN(filterValues[1])) {
                    queryString += 'lte';
                    queryValue =  filterValues[1];
                } else if (isNaN(filterValues[1]) && !isNaN(filterValues[0])) {
                    queryString += 'gte';
                    queryValue = filterValues[0];
                } else if (!isNaN(filterValues[0]) && !isNaN(filterValues[1])) {
                    if (filterValues[0] <= filterValues[1]) {
                        queryString += 'range';
                        queryValue = filterValues[0] + ',' + filterValues[1];
                    }
                }

                for (var oldFilterLabel in $scope.filtering) {
                    if ($scope.filtering.hasOwnProperty(oldFilterLabel) && oldFilterLabel.startsWith(filterLabel)) {
                        delete $scope.filtering[oldFilterLabel];

                        break;
                    }
                }

                if (typeof queryValue !== 'undefined') {
                    $scope.filtering[queryString] = queryValue;
                }

                filter.pristine = true;
            };

            var clearListFilters = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.selected = [];

                    delete $scope.filtering[filter.filter_name];
                });
            };

            $scope.clearRangeFilter = function (filter, filterLabel) {
                filter.values = ['', ''];

                for (var oldFilterLabel in $scope.filtering) {
                    if ($scope.filtering.hasOwnProperty(oldFilterLabel) && oldFilterLabel.startsWith(filterLabel)) {
                        delete $scope.filtering[oldFilterLabel];

                        break;
                    }
                }

                filter.pristine = true;
            };

            var clearRangeFilters = function () {
                angular.forEach($scope.rangeFilters, function (filter, filterLabel) {
                    $scope.clearRangeFilter(filter, filterLabel);
                });
            };

            $scope.clearFilters = function () {
                clearListFilters();
                clearRangeFilters();
            };

            function filter () {
                $scope.resource.get($scope.filtering, function (data) {
                    $scope.model = data;
                });
            }

            $scope.$watch('ordering', function (newVal, oldVal) {
                if (newVal != oldVal) {
                    $scope.filtering.ordering = ($scope.ordering.ascending ? '' : '-') + $scope.ordering.field;
                }
            }, true);

            var timeoutPromise;

            $scope.$watch('[filtering, currentPage]', function (newVal, oldVal) {
                if (newVal != oldVal) {
                    $timeout.cancel(timeoutPromise);

                    timeoutPromise = $timeout(function() {
                        if (newVal[1] != oldVal[1]) {
                            $scope.filtering.page = $scope.currentPage;
                        } else {
                            if (newVal[0].page != oldVal[0].page) {
                                filter();
                            } else {
                                if ($scope.currentPage != 1) {
                                    $scope.currentPage = 1;
                                } else {
                                    filter();
                                }
                            }
                        }
                    }, 100);
                }
            }, true);
        }
    };
});
