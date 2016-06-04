app.factory('Suits', function ($resource) {
    return $resource('/api/suits/:id', { id: '@id' });
});
