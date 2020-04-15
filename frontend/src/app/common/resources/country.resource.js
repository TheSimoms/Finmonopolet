app.factory('Country', function ($resource, API_HOST) {
    return $resource(`${API_HOST}/api/countries/:id`, { id: '@id' });
});
