app.directive('pie', function () {
    return {
        restrict: 'E',
        scope: {
            score: '@',
            text: '@',
            size: '@',
        },
        templateUrl: 'static/app/common/directives/pie/pie.template.html',
        link: function ($scope) {
            $scope.svgStyle = {};

            if ($scope.size) {
                $scope.svgStyle.height = $scope.size + 'px';
                $scope.svgStyle.width = $scope.size + 'px';
            }

            $scope.circleStyle = {
                'stroke-dasharray': ($scope.score / 12 * 100) + ' 100'
            };
        }
    };
});
