app.directive('itemList', function ($q, $timeout, Product, Category, Country, Producer, Suits, Selection) {
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
            $scope.numberOfSelectedFilters = 0;

            $scope.filtering = $scope.lockedFilters || {};
            $scope.loading = true;

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

            function listFilter (title, filter_name, resource) {
                return {
                    title: title, filter_name: filter_name, resource: resource, data: [], selected: [],
                    filtering: { search: '', page: 1 }, counter: 0
                };
            }

            function rangeFilter (title, filter_name, unit) {
                return  {
                    title: title, filter_name: filter_name, unit: unit, displayText: '', values: ['', '']
                };
            }

            $scope.filters = {
                category: listFilter('Varegruppe', 'category', Category),
                producer: listFilter('Produsent', 'producer', Producer),
                suits: listFilter('Passer til', 'suits', Suits),
                selection: listFilter('Produktutvalg', 'selection', Selection)
            };

            $scope.rangeFilters = {
                price: rangeFilter('Pris', 'price', ',-'),
                volume: rangeFilter('Volum', 'volume', ' l'),
                alcohol: rangeFilter('Alkoholinnhold', 'alcohol', ' %'),
                litre_price: rangeFilter('Pris pr. liter', 'litre_price', ',- pr. l'),
                alcohol_price: rangeFilter('Pris pr. %', 'alcohol_price', ',- pr. %')
            };

            if (typeof $scope.lockedFilters !== 'undefined') {
                angular.forEach(Object.keys($scope.lockedFilters), function (filter) {
                    delete $scope.filters[filter];
                });
            }

            $scope.updateListFilter = function (filter, item) {
                var index = filter.selected.indexOf(item);

                if (index >= 0) {
                    filter.selected.splice(index, 1);

                    $scope.numberOfSelectedFilters -= 1;
                } else {
                    filter.selected.push(item);

                    $scope.numberOfSelectedFilters += 1;
                }

                if (filter.selected.length == 0) {
                    delete $scope.filtering[filter.filter_name];
                } else {
                    $scope.filtering[filter.filter_name] = filter.selected.map(function (item) {
                        return item.id;
                    }).join();
                }
            };

            function setFilterString (filter) {
                var filterValues = [parseFloat(filter.values[0]), parseFloat(filter.values[1])];

                filter.displayText = '';

                if (isNaN(filterValues[0]) && !isNaN(filterValues[1])) {
                    filter.displayText = 'Under ' +  filterValues[1];
                } else if (isNaN(filterValues[1]) && !isNaN(filterValues[0])) {
                    filter.displayText = 'Over ' + filterValues[0];
                } else if (!isNaN(filterValues[0]) && !isNaN(filterValues[1])) {
                    if (filterValues[0] <= filterValues[1]) {
                        filter.displayText = filterValues[0] + ' - ' + filterValues[1];
                    }
                }
            }

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

                var hasOldFilter = false;

                for (var oldFilterLabel in $scope.filtering) {
                    if ($scope.filtering.hasOwnProperty(oldFilterLabel) && oldFilterLabel.startsWith(filterLabel)) {
                        delete $scope.filtering[oldFilterLabel];

                        hasOldFilter = true;

                        break;
                    }
                }

                if (typeof queryValue !== 'undefined') {
                    $scope.filtering[queryString] = queryValue;

                    if (!hasOldFilter) {
                        $scope.numberOfSelectedFilters += 1;
                    }
                } else if (hasOldFilter) {
                    $scope.numberOfSelectedFilters -= 1;
                }

                setFilterString(filter);
            };

            var clearListFilters = function () {
                angular.forEach($scope.filters, function (filter) {
                    filter.selected = [];

                    delete $scope.filtering[filter.filter_name];
                });
            };

            $scope.clearRangeFilter = function (filter, filterLabel) {
                filter.values = ['', ''];
                filter.displayText = '';

                $scope.numberOfSelectedFilters -= 1;

                for (var oldFilterLabel in $scope.filtering) {
                    if ($scope.filtering.hasOwnProperty(oldFilterLabel) && oldFilterLabel.startsWith(filterLabel)) {
                        delete $scope.filtering[oldFilterLabel];

                        break;
                    }
                }
            };

            var clearRangeFilters = function () {
                angular.forEach($scope.rangeFilters, function (filter, filterLabel) {
                    $scope.clearRangeFilter(filter, filterLabel);
                });
            };

            $scope.clearFilters = function () {
                clearListFilters();
                clearRangeFilters();

                $scope.numberOfSelectedFilters = 0;
            };

            $scope.itemSelected = function (filter, item) {
                return filter.selected.indexOf(item) !== -1;
            };

            var globalFilterCounter = 0;

            function filter () {
                globalFilterCounter = (globalFilterCounter + 1) % 100;

                var currentCounter = globalFilterCounter;

                $scope.loading = true;

                $scope.resource.get($scope.filtering, function (data) {
                    if (globalFilterCounter === currentCounter) {
                        $scope.loading = false;

                        $scope.model = data;
                    }
                });
            }

            $scope.search = function (search) {
                $scope.filtering.search = search.toLowerCase();
            };

            angular.forEach($scope.filters, function (filter, filterLabel) {
                var filterTimeoutPromise;

                $scope.$watch('filters.' + filterLabel + '.filtering', function (newVal, oldVal) {
                    $timeout.cancel(filterTimeoutPromise);

                    filterTimeoutPromise = $timeout(function() {
                        if (newVal.search !== oldVal.search) {
                            if (newVal.page !== 1) {
                                newVal.page = 1;

                                return;
                            }
                        }

                        filter.counter = (filter.counter + 1) % 100;

                        var currentCounter = filter.counter;

                        filter.resource.get(filter.filtering, function (data) {
                            if (currentCounter === filter.counter) {
                                filter.data = data;
                            }
                        });
                    }, 100);
                }, true);
            });

            $scope.$watch('ordering', function (newVal, oldVal) {
                if (!angular.equals(newVal, oldVal)) {
                    $scope.filtering.ordering = ($scope.ordering.ascending ? '' : '-') + $scope.ordering.field;
                }
            }, true);

            var timeoutPromise;

            $scope.$watch('[filtering, currentPage]', function (newVal, oldVal) {
                $timeout.cancel(timeoutPromise);

                timeoutPromise = $timeout(function() {
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
