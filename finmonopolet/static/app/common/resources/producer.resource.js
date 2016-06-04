app.factory('Producer', function ($resource) {
    return $resource('/api/producers/:id', { id: '@id' });
});
