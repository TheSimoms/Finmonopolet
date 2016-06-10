app.factory('Selection', function ($resource) {
    return $resource('/api/selections/:id', { id: '@id' });
});
