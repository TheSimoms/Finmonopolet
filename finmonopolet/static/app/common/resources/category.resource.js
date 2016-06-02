app.factory('Category', function ($resource) {
    return $resource('/api/categories/:view/:id',
        { view: 'paged', id: '@id' },
        {
            getAll: { method: 'GET', isArray: true, params: { view: 'full' } }
        });
});
