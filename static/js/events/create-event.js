GoFriend.controller('createEvent', function ($scope, $dragon, $q, $timeout) {

    $dragon.onReady(function () {
        $scope.channel = 'events-channel';
        $dragon.subscribe('events', $scope.channel, {});

        $dragon.onChannelMessage(function (channels, message) {
            $dragon.getList('events').then(function (response) {
                console.log(response);
            });
        });

        $scope.open = function ($event) {
            $scope.status.opened = true;
            console.log($scope.status.opened);
        };
        $scope.status = {
            opened: false
        };

        $scope.finished = function () {
            $scope.form.dateTime = new Date($scope.date);
            $dragon.create('events', $scope.form).then(function (response) {
                console.log(response); // a newly created Foo
            });
        };

        $scope.categories = [
            'Business',
            'Crafts',
            'Education',
            'Family',
            'Fashion',
            'Fitness',
            'Food',
            'Learning',
            'Literature',
            'Gaming',
            'Music',
            'Outdoor',
            'Pets',
            'Photography',
            'Politics',
            'Technology',
            'Television',
            'Special',
            'Spiritual',
            'Sports',
            'Writing'
        ];

        //$scope.form.cat = $scope.categories[0]


        $scope.date = new Date().setMinutes(0);


        $scope.minDate = new Date();
        var maxMonth = $scope.minDate.getMonth() + 6;
        $scope.maxDate = new Date();
        $scope.maxDate.setMonth(maxMonth);

        $scope.dateOptions = {
            startingDay: 1,
            showWeeks: false
        };

        $scope.hourStep = 1;
        $scope.minuteStep = 15;


        $scope.showMeridian = true;
    });

});