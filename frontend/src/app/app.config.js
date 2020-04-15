app.config(function ($locationProvider) {
    $locationProvider.html5Mode(true);
});

app.config(function ($urlMatcherFactoryProvider) {
    $urlMatcherFactoryProvider.strictMode(false);
});
