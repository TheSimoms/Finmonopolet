app.factory('Country', function ($resource) {
    return $resource('/api/countries/:id', { id: '@id' });
});
