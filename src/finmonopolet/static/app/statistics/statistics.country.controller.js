

app.controller('StatisticsCountryCtrl', function ($scope, country, statistics) {
    $scope.country = country;

    statistics.$promise.then(function() {
        // Parse country price development for ng-chart
        var price_development = new Object();

        price_development.data = [];
        price_development.data.push([],[],[]);

        price_development.series = ["Gjennomsnitt", "Billigst", "Dyrest"];

        price_development.options = {elements: {line: {fill: false}}} //TODO: Options not working

        price_development.labels = [];

        for (entry of statistics) {
            // Entry data
            price_development.data[0].push(entry.price.avg);
            price_development.data[1].push(entry.price.min);
            price_development.data[2].push(entry.price.max);

            // Entry label
            var date_formatted = new Date("2016-07-31T18:50:36.84Z")
                .toLocaleDateString();
            price_development.labels.push(date_formatted);

        }

        $scope.price_development = price_development;
    });
});
