app.config(
    function config($locationProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
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
                url: '/assortment',
                template: '<div ui-view></div>',
                abstract: true
            })
            .state('assortment.list', {
                url: '',
                templateUrl: 'static/app/assortment/assortment.view.html',
                controller: 'AssortmentCtrl',
                resolve: {
                    categories: function (Category) {
                        return Category.get();
                    },
                    products: function (Product) {
                        return Product.get();
                    }
                },
                ncyBreadcrumb: {
                    label: 'Vareutvalg'
                }
            })
            .state('assortment.category', {
                url: '/category/{categoryId:int}',
                templateUrl: 'static/app/assortment/category/category.details.view.html',
                controller: 'CategoryDetailCtrl',
                resolve: {
                    category: function ($stateParams, Category) {
                        return Category.get({id: $stateParams['categoryId']});
                    },
                    products: function ($stateParams, Product) {
                        return Product.get({category: $stateParams['categoryId']});
                    }
                },
                ncyBreadcrumb: {
                    parent: 'assortment.list',
                    label: '{{ category.name }}'
                }
            })
            .state('assortment.product', {
                url: '/product/{productId:int}',
                templateUrl: 'static/app/assortment/product/product.details.view.html',
                controller: 'ProductDetailCtrl',
                resolve: {
                    product: function ($stateParams, Product) {
                        return Product.get({id: $stateParams['productId']});
                    }
                },
                ncyBreadcrumb: {
                    // FIXME: Add category as parent
                    parent: 'assortment.list',
                    label: '{{ product.name }}'
                }
            })
            .state('statistics', {
                url: '/statistics',
                template: '<div ui-view></div>',
                abstract: true
            })
            .state('statistics.list', {
                url: '',
                templateUrl: 'static/app/statistics/statistics.view.html',
                controller: 'StatisticsCtrl',
                resolve: {
                    category: function () {
                        return null;
                    },
                    statistics: function (Statistics) {
                        return Statistics.get();
                    }
                },
                ncyBreadcrumb: {
                    label: 'Statistikk'
                }
            })
            .state('statistics.details', {
                url: '/category/{categoryId:int}',
                templateUrl: 'static/app/statistics/statistics.view.html',
                controller: 'StatisticsCtrl',
                resolve: {
                    category: function ($stateParams, Category) {
                        return Category.get({id: $stateParams['categoryId']});
                    },
                    statistics: function ($stateParams, Statistics) {
                        return Statistics.get({category: $stateParams['categoryId']});
                    }
                },
                ncyBreadcrumb: {
                    parent: 'statistics.list',
                    label: '{{ category.name }}'
                }
            })
            .state('store', {
                url: '/store',
                template: '<div ui-view></div>',
                abstract: true
            })
            .state('store.list', {
                url: '',
                templateUrl: 'static/app/store/store.list.view.html',
                controller: 'StoreListCtrl',
                resolve: {
                    stores: function (Store) {
                        return Store.query();
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
