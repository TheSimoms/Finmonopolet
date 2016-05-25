app.factory('Category', function ($resource) {
    return $resource('/api/categories/:id', {id: '@id'});
});
