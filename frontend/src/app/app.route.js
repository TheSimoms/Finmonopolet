app.config(function ($stateProvider, $urlRouterProvider)  {
    function productPage(url, resource, filter) {
        return {
            url: '/' + url + '/{id:int}',
            templateUrl: '/app/assortment/assortment.details.view.html',
            controller: 'AssortmentDetailsController',
            resolve: {
                resource: () => resource,
                filter: () => filter
            },
            ncyBreadcrumb: {
                parent: 'assortment.list',
                label: '{{ item.name }}'
            }
        };
    }

    $urlRouterProvider.otherwise('/');

    $stateProvider
        .state('assortment', {
            url: '',
            template: '<div ui-view></div>',
            abstract: true
        })
        .state('assortment.list', {
            url: '',
            templateUrl: '/app/assortment/assortment.details.view.html',
            ncyBreadcrumb: {
                label: 'Vareutvalg'
            }
        })
        .state('assortment.productType', productPage('varegrupper', 'ProductType', 'product_type'))
        .state('assortment.country', productPage('land', 'Country', 'country'))
        .state('assortment.producer', productPage('produsenter', 'Producer', 'producer'))
});
