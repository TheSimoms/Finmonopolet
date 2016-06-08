app.factory('Product', function ($resource) {
    return $resource('/api/products/:id', { id: '@id' });
});
