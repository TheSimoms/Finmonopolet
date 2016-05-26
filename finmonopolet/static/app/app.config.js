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
                controller: 'FrontPageCtrl',
                title: '',
                ncyBreadcrumb: {
                    label: 'Hjem'
                }
            })
            .state('category', {
                url: '/category',
                template: '<div ui-view></div>',
                abstract: true
            })
            .state('category.list', {
                url: '',
                templateUrl: 'static/app/category/category.list.view.html',
                controller: 'CategoryListCtrl',
                title: 'Kategorier',
                resolve: {
                    categories: function (Category) {
                        return Category.get();
                    }
                },
                ncyBreadcrumb: {
                    label: 'Kategorier'
                }
            })
            .state('category.details', {
                url: '/{categoryId:int}',
                templateUrl: 'static/app/category/category.details.view.html',
                controller: 'CategoryDetailCtrl',
                title: 'Derp',
                parent: 'category',
                resolve: {
                    category: function ($stateParams, Category) {
                        return Category.get({id: $stateParams['categoryId']});
                    },
                    products: function ($stateParams, Product) {
                        return Product.get({category: $stateParams['categoryId']});
                    }
                },
                ncyBreadcrumb: {
                    parent: 'category.list',
                    label: '{{ category.name }}'
                }
            });
    }
);
