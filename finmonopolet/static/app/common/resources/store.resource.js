app.factory('Store', function ($resource) {
    return $resource('/api/stores/:view/:id',
        { view: 'information', id: '@id' },
        {
            getLocations: { method: 'GET', isArray: true, params: { view: 'locations' } }
        }
    );
});
