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
                template: '<item-list model="products" resource="productResource"></item-list>',
                controller: function ($scope, Product, products) {
                    $scope.products = products;
                    $scope.productResource = Product;
                },
                resolve: {
                    products: function (Product) {
                        return Product.get();
                    }
                },
                ncyBreadcrumb: {
                    label: 'Vareutvalg'
                }
            })
            .state('assortment.category', {
                url: '/varegrupper/{categoryId:int}',
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
                url: '/varer/{productId:int}',
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
                url: '/statistikk',
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
                url: '/varegrupper/{categoryId:int}',
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
