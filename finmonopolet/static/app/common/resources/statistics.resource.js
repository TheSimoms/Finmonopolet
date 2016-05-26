app.factory('Statistics', function ($resource) {
    return $resource('/api/statistics');
});
