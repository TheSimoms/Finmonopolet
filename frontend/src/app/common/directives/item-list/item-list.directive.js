app.directive('itemList', function ($q, $timeout, Product, ProductType, Country, Producer, Selection) {
    return {
        restrict: 'E',
        scope: {
            title: '=?',
            lockedFilters: '=?',
            itemsPerPage: '=?'
        },
        templateUrl: '/app/common/directives/item-list/item-list.template.html',
        link: function ($scope) {
            const LIST = 'list';
            const RANGE = 'range';

            $scope.LIST = LIST;
            $scope.RANGE = RANGE;

            $scope.resource = Product;
            $scope.filtering = $scope.lockedFilters || {};
            $scope.ordering = { field: 'alcohol_price', ascending: true };
            $scope.itemsPerPage = $scope.itemsPerPage || 12;
            $scope.currentPage = 1;
            $scope.loading = true;

            $scope.filtering = Object.assign($scope.filtering, {
                search: '',
                page: 1
            });

            $scope.orderingFields = {
                'canonical_name': 'Navn',
                'product_type': 'Varegruppe',
                'country': 'Land',
                'producer': 'Produsent',
                'volume': 'Volum',
                'alcohol_content': 'Alkoholinnhold',
                'price': 'Pris',
                'litre_price': 'Pris pr. liter',
                'alcohol_price': 'Pris pr. liter alkohol',
            };

            function listFilter (title, filter_name, resource) {
                return {
                    title: title, filter_name: filter_name, resource: resource, data: [], selected: [],
                    filtering: { search: '', page: 1 }, search: '', counter: 0, type: LIST,
                };
            }

            function rangeFilter (title, filter_name, unit) {
                return  {
                    title: title, filter_name: filter_name, unit: unit, values: ['', ''], type: RANGE,
                };
            }

            $scope.filters = [
                rangeFilter('Volum', 'volume', ' l'),
                rangeFilter('Alkoholinnhold', 'alcohol_content', ' %'),
                rangeFilter('Pris', 'price', ',-'),
                rangeFilter('Pris pr. liter', 'litre_price', ',- pr. l'),
                rangeFilter('Pris pr. liter alkohol', 'alcohol_price', ',- pr. l'),
                listFilter('Varegruppe', 'product_type', ProductType),
                listFilter('Land', 'country', Country),
                listFilter('Produsent', 'producer', Producer),
            ];

            if (typeof $scope.lockedFilters !== 'undefined') {
                $scope.filters = $scope.filters.filter(
                    filter => !$scope.lockedFilters.hasOwnProperty(filter.filter_name)
                );
            }

            $scope.updateListFilter = (filter, item) => {
                var index = filter.selected.indexOf(item);

                if (index >= 0) {
                    filter.selected.splice(index, 1);
                } else {
                    filter.selected.push(item);
                }

                if (filter.selected.length === 0) {
                    delete $scope.filtering[filter.filter_name];
                } else {
                    $scope.filtering[filter.filter_name] = filter.selected.map(item => item.id).join();
                }
            };

            $scope.updateRangeFilter = (filter) => {
                var queryString = filter.filter_name + '__';
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

                var hasOldFilter = false;

                for (var filterLabel in $scope.filtering) {
                    if ($scope.filtering.hasOwnProperty(filterLabel) && filterLabel.startsWith(filter.filter_name)) {
                        delete $scope.filtering[filterLabel];

                        hasOldFilter = true;

                        break;
                    }
                }

                if (typeof queryValue !== 'undefined') {
                    $scope.filtering[queryString] = queryValue;
                }
            };

            $scope.clearFilters = function () {
                clearListFilters();
                clearRangeFilters();
            };

            function clearListFilters() {
                $scope.filters.filter(filter => filter.type === $scope.LIST).forEach(filter => {
                    filter.selected = [];

                    delete $scope.filtering[filter.filter_name];
                });
            }

            function clearRangeFilters() {
                $scope.filters.filter(filter => filter.type === $scope.RANGE).forEach(filter => {
                    filter.values = ['', ''];

                    for (var filterLabel in $scope.filtering) {
                        if ($scope.filtering.hasOwnProperty(filterLabel) && filterLabel.startsWith(filter.filter_name)) {
                            delete $scope.filtering[filterLabel];

                            break;
                        }
                    }
                });
            }

            $scope.itemSelected = (filter, item) => filter.selected.indexOf(item) !== -1;

            var globalFilterCounter = 0;

            function filter() {
                globalFilterCounter = (globalFilterCounter + 1) % 100;

                var currentCounter = globalFilterCounter;

                $scope.loading = true;

                $scope.resource.get($scope.filtering, (data) => {
                    if (globalFilterCounter === currentCounter) {
                        $scope.loading = false;

                        $scope.model = data;
                    }
                });
            }

            $scope.search = (search) => {
                $scope.filtering.search = search.toLowerCase();
            };

            $scope.filters.forEach((filter, index) => {
                if (filter.type !== $scope.LIST) {
                    return;
                }

                var filterTimeoutPromise;

                $scope.$watch('filters[' + index + '].search', (newVal, oldVal) => {
                    if (newVal !== oldVal) {
                        filter.filtering.search = newVal.toLowerCase();
                    }
                });

                $scope.$watch('filters[' + index + '].filtering', (newVal, oldVal) => {
                    $timeout.cancel(filterTimeoutPromise);

                    filterTimeoutPromise = $timeout(() => {
                        if (newVal.search !== oldVal.search) {
                            if (newVal.page !== 1) {
                                newVal.page = 1;

                                return;
                            }
                        }

                        filter.counter = (filter.counter + 1) % 100;

                        var currentCounter = filter.counter;

                        filter.resource.get(filter.filtering, (data) => {
                            if (currentCounter === filter.counter) {
                                filter.data = data;
                            }
                        });
                    }, 100);
                }, true);
            });

            $scope.$watch('ordering', (newVal) => {
                $scope.filtering.ordering = ($scope.ordering.ascending ? '' : '-') + $scope.ordering.field;
            }, true);

            var timeoutPromise;

            $scope.$watch('[filtering, currentPage]', (newVal, oldVal) => {
                $timeout.cancel(timeoutPromise);

                timeoutPromise = $timeout(() => {
                    if (newVal[1] !== oldVal[1]) {
                        $scope.filtering.page = $scope.currentPage;
                    } else {
                        if (newVal[0].page !== oldVal[0].page) {
                            filter();
                        } else {
                            if ($scope.currentPage !== 1) {
                                $scope.currentPage = 1;
                            } else {
                                filter();
                            }
                        }
                    }
                }, 100);
            }, true);
        }
    };
});
