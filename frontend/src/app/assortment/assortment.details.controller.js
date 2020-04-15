app.controller('AssortmentDetailsController', function($scope, $stateParams, $injector, resource, filter) {
    $scope.filters = {};

    $scope.filters[filter] = $stateParams.id;

    $scope.item = $injector.get(resource).get({ id: $stateParams.id }, item => {
        $scope.title = item.name;
    });
});
