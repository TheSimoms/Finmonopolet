app.factory('Producer', function ($resource, API_HOST) {
    return $resource(`${API_HOST}/api/producers/:id`, { id: '@id' });
});
