app.config(
    function config($locationProvider) {
        $locationProvider.html5Mode(true);
    }
);

app.config(
    function($breadcrumbProvider) {
        $breadcrumbProvider.setOptions({
            prefixStateName: 'home'
        });
    }
);

app.config(
    function config($urlMatcherFactoryProvider) {
        $urlMatcherFactoryProvider.strictMode(false);
    }
);

app.config(
    function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');

        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: 'static/app/front-page/front-page.view.html',
                ncyBreadcrumb: {
                    label: 'Hjem'
                }
            })
            .state('assortment', {
                url: '/vareutvalg',
                template: '<div ui-view></div>',
                abstract: true
            })
            .state('assortment.list', {
                url: '',
                templateUrl: 'static/app/assortment/assortment.details.view.html',
                ncyBreadcrumb: {
                    label: 'Vareutvalg'
                }
            })
            .state('assortment.category', {
                url: '/varegrupper/{categoryId:int}',
                templateUrl: 'static/app/assortment/assortment.details.view.html',
                controller: function ($scope, $stateParams, Category) {
                    $scope.filters = {
                        category: $stateParams.categoryId
                    };

                    $scope.category = Category.get({ id: $stateParams.categoryId }, function (category) {
                        $scope.title = category.name;
                    });
                },
                ncyBreadcrumb: {
                    parent: 'assortment.list',
                    label: '{{ category.name }}'
                }
            })
            .state('assortment.product', {
                url: '/varer/{productId:int}',
                templateUrl: 'static/app/assortment/product/product.details.view.html',
                controller: function ($scope, $stateParams, Product) {
                    $scope.product = Product.get({ id: $stateParams.productId });
                },
                ncyBreadcrumb: {
                    parent: 'assortment.list',
                    label: '{{ product.name }}'
                }
            })
            .state('assortment.country', {
                url: '/land/{countryId:int}',
                templateUrl: 'static/app/assortment/assortment.details.view.html',
                controller: function ($scope, $stateParams, Country) {
                    $scope.filters = {
                        country: $stateParams.countryId
                    };

                    $scope.country = Country.get({ id: $stateParams.countryId }, function (country) {
                        $scope.title = country.name;
                    });
                },
                ncyBreadcrumb: {
                    parent: 'assortment.list',
                    label: '{{ country.name }}'
                }
            })
            .state('assortment.producer', {
                url: '/produsenter/{producerId:int}',
                templateUrl: 'static/app/assortment/assortment.details.view.html',
                controller: function ($scope, $stateParams, Producer) {
                    $scope.filters = {
                        producer: $stateParams.producerId
                    };

                    $scope.producer = Producer.get({ id: $stateParams.producerId}, function (producer) {
                        $scope.title = producer.name;
                    });
                },
                ncyBreadcrumb: {
                    parent: 'assortment.list',
                    label: '{{ producer.name }}'
                }
            })
            .state('statistics', {
                url: '/statistikk',
                template: '<div ui-view></div>',
                abstract: true
            })
            .state('statistics.list', {
                url: '',
                templateUrl: 'static/app/statistics/statistics.view.html',
                controller: 'StatisticsCtrl',
                resolve: {
                    statistics: function (Statistics) {
                        return Statistics.query();
                    },
                    category: function (Category) {
                        return Category.get();
                    },
                    country: function (Country) {
                        return Country.get();
                    }

                },
                ncyBreadcrumb: {
                    label: 'Statistikk'
                }
            })
            .state('statistics.country', {
                url: '/land/{countryId:int}',
                templateUrl: 'static/app/statistics/statistics.country.view.html',
                controller: 'StatisticsCountryCtrl',
                resolve: {
                    country: function ($stateParams, Country) {
                        return Country.get({id: $stateParams['countryId']});
                    },
                    statistics: function ($stateParams, Statistics) {
                        return Statistics.query({country: $stateParams['countryId']});
                    }
                },
                ncyBreadcrumb: {
                    parent: 'statistics.list',
                    label: '{{ country.name }}'
                }
            })
            .state('statistics.category', {
                url: '/varegrupper/{categoryId:int}',
                templateUrl: 'static/app/statistics/statistics.category.view.html',
                controller: 'StatisticsCategoryCtrl',
                resolve: {
                    category: function ($stateParams, Category) {
                        return Category.get({id: $stateParams['categoryId']});
                    },
                    statistics: function ($stateParams, Statistics) {
                        return Statistics.query({category: $stateParams['categoryId']});
                    }
                },
                ncyBreadcrumb: {
                    parent: 'statistics.list',
                    label: '{{ category.name }}'
                }
            })
            .state('store', {
                url: '/butikker',
                template: '<div ui-view></div>',
                abstract: true
            })
            .state('store.list', {
                url: '',
                templateUrl: 'static/app/store/store.list.view.html',
                controller: 'StoreListCtrl',
                resolve: {
                    stores: function (Store) {
                        return Store.get();
                    },
                    storeLocations: function (Store) {
                        return Store.getLocations();
                    }
                },
                ncyBreadcrumb: {
                    label: 'Butikker'
                }
            })
            .state('store.details', {
                url: '/{storeId:int}',
                templateUrl: 'static/app/store/store.details.view.html',
                controller: 'StoreDetailsCtrl',
                resolve: {
                    store: function ($stateParams, Store) {
                        return Store.get({id: $stateParams['storeId']});
                    }
                },
                ncyBreadcrumb: {
                    parent: 'store.list',
                    label: '{{ store.name }}'
                }
            });
    }
);
