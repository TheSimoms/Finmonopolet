app.factory('Selection', function ($resource, API_HOST) {
    return $resource(`${API_HOST}/api/selections/:id`, { id: '@id' });
});
