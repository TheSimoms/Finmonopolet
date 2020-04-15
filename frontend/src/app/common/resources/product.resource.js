app.factory('Product', function ($resource, API_HOST) {
    return $resource(`${API_HOST}/api/products/:id`, { id: '@id' });
});
