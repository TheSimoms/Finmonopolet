app.factory('ProductType', function ($resource, API_HOST) {
    return $resource(`${API_HOST}/api/product_types/:id`, { id: '@id' });
});
