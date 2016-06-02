app.factory('Statistics', function ($resource) {
    return $resource('/api/statistics/:view',
        { view: 'full' },
        {
            getRanges: { method: 'GET', params: { view: 'ranges' } }
        }
    );
});
