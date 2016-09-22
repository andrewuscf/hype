GoFriend.controller('settingsController',
    function ($scope, $q, $http) {
        $scope.form = {
            user: {}
        };

        $http.get(window.location.origin + '/api/v1/user/settings').success(function (result) {
            $scope.form.user.username = result.user.username;
            $scope.form.user.first_name = result.user.first_name;
            $scope.form.user.last_name = result.user.last_name;
            $scope.form.bio = result.bio;

        });

        $scope.settingsForm = function () {
            $http.put(window.location.origin + '/api/v1/user/settings', $scope.form).success(function (result, status) {
                if(status ==200)
                    window.location = window.location.origin + '/user/'+ $scope.form.user.username;
            })
        }
    });