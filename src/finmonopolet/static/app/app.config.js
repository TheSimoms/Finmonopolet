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
        function productPage (url, resource, filter) {
            return {
                url: '/' + url + '/{id:int}',
                templateUrl: '/static/app/assortment/assortment.details.view.html',
                controller: function ($scope, $stateParams, $injector) {
                    $scope.filters = {};

                    $scope.filters[filter] = $stateParams.id;

                    $scope.item = $injector.get(resource).get({ id: $stateParams.id }, function (item) {
                        $scope.title = item.name;
                    });
                },
                ncyBreadcrumb: {
                    parent: 'assortment.list',
                    label: '{{ item.name }}'
                }
            };
        }

        $urlRouterProvider.otherwise('/');

        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: '/static/app/front-page/front-page.view.html',
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
                templateUrl: '/static/app/assortment/assortment.details.view.html',
                ncyBreadcrumb: {
                    label: 'Vareutvalg'
                }
            })
            .state('assortment.category', productPage('varegrupper', 'Category', 'category'))
            .state('assortment.country', productPage('land', 'Country', 'country'))
            .state('assortment.producer', productPage('produsenter', 'Producer', 'producer'))
            .state('assortment.product', {
                url: '/varer/{productId:int}',
                templateUrl: '/static/app/assortment/product/product.details.view.html',
                controller: function ($scope, $stateParams, Product) {
                    $scope.product = Product.get({ id: $stateParams.productId });

                    $scope.characteristics = [
                        { id: 'fullness', title: 'Fylde' },
                        { id: 'freshness', title: 'Friskhet' },
                        { id: 'tannins', title: 'Garvestoffer' },
                        { id: 'bitterness', title: 'Bitterhet' },
                        { id: 'sweetness', title: 'Sødme' },
                    ];

                    $scope.suits = {
                        'Dessert, kake, frukt': 'cupcake.svg',
                        'Storfe': 'cow.svg',
                        'Fisk': 'fish.svg',
                        'Grønnsaker': 'broccoli.svg',
                        'Lam og sau': 'sheep.svg',
                        'Storvilt': 'deer.svg',
                        'Skalldyr': 'big-crab.svg',
                        'Småvilt og fugl': 'rabbit.svg',
                        'Aperitiff/avec': 'wine-glass.svg',
                        'Svinekjøtt': 'pig-head.svg',
                        'Ost': 'piece-of-cheese.svg',
                        'Lyst kjøtt': 'chicken.svg',
                    };

                    $scope.showCharactistics = false;

                    $scope.product.$promise.then(function () {
                        for (var i = 0; i < $scope.characteristics.length; i++) {
                            if ($scope.product[$scope.characteristics[i].id] !== null) {
                                $scope.showCharactistics = true;

                                return;
                            }
                        }
                    });
                },
                ncyBreadcrumb: {
                    parent: 'assortment.list',
                    label: '{{ product.name }}'
                }
            })
            .state('statistics', {
                url: '/statistikk',
                template: '<div ui-view></div>',
                abstract: true
            })
            .state('statistics.list', {
                url: '',
                templateUrl: '/static/app/statistics/statistics.view.html',
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
                templateUrl: '/static/app/statistics/statistics.country.view.html',
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
                templateUrl: '/static/app/statistics/statistics.category.view.html',
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
                templateUrl: '/static/app/store/store.list.view.html',
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
                templateUrl: '/static/app/store/store.details.view.html',
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
