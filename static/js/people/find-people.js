"use strict";
GoFriend.controller('listController',
    function($scope, $dragon,$q,$timeout, userInfo, related) {
        String.prototype.capitalize = function() {
            return this.charAt(0).toUpperCase() + this.slice(1);
        };
        $scope.channel = 'swampy-channel';
        $scope.users_on_map = [];

        var deffered = $q.defer();

        var subscribeToChannels = function(){
            $dragon.subscribe('locationcurrent', $scope.channel, {});
        };

        var Setup = function(){
            $dragon.getSingle('locationcurrent', {user: user}).then(function (response) {
                var userLocationData = response.data;
                $scope.myLocation = new google.maps.LatLng(userLocationData.latitude, userLocationData.longitude);


                $dragon.getList('locationcurrent', {latitude:userLocationData.latitude,longitude: userLocationData.longitude, user: user}).then(function(response){
                    $scope.nearUsers = response.data;
                });
            });
        };

        var mapSetup = function(near_users){
            var mapOptions = {
                zoom: 14,
                center: $scope.myLocation,
                mapTypeId: google.maps.MapTypeId.TERRAIN
            };

            $scope.map = new google.maps.Map(document.getElementById('map'), mapOptions);

            $scope.markers = [];

            var infoWindow = new google.maps.InfoWindow();


            var createMarker = function (user){
                var userInfo = user.info;
                var totalRelated = userInfo.interests.length + userInfo.subscriptions.length + userInfo.music.length;
                var marker = new google.maps.Marker({
                    map: $scope.map,
                    position: new google.maps.LatLng(user.lat, user.long),
                    username: user.info.username,
                    id: user.user,
                    bio: user.info.profile.bio,
                    interests: user.info.interests,
                    music: user.info.music,
                    photos: user.info.photos,
                    profilePhoto: user.info.profile.avatar_url,
                    subs: user.info.subscriptions,
                    age: user.info.profile.age,
                    total: totalRelated,
                    open:false
                });

                marker.content = '<div class="infoWindowContent">' + user.id + '</div>';

                google.maps.event.addListener(marker, 'click', function(){
                    if(marker.open == true){
                        $timeout(function() {
                            infoWindow.close($scope.map, marker);
                            $scope.$apply(marker.open = false);
                        })
                    }else{
                        infoWindow.setContent('<h2 class="markerTitle">' + marker.username.capitalize() + '</h2>' +
                        '<br/>');
                        infoWindow.open($scope.map, marker);
                        $scope.$apply(marker.open = true);
                    }
                });

                $scope.markers.push(marker);
            };

            $scope.openInfoWindow = function(event, selectedMarker){
                event.preventDefault();
                //google.maps.event.trigger(selectedMarker, 'click');
                if(selectedMarker.open != true){
                    infoWindow.setContent('<h2 class="markerTitle text-center">' + selectedMarker.username.capitalize() + '</h2>' +
                        '<br/>');
                    infoWindow.open($scope.map, selectedMarker);
                    $('#panel'+selectedMarker.id).removeClass('hidden');
                    selectedMarker.open = true;
                }else{
                    infoWindow.close($scope.map, selectedMarker);
                    $('#panel'+selectedMarker.id).addClass('hidden');
                    selectedMarker.open = false;
                }
            };

            near_users.forEach(function(person){
                createMarker(person);
            });
        };

        var relatedData = function(){
            var near_users= [];
            var deffered = $q.defer();
            var prom = [];
            $scope.nearUsers.forEach(function(eachOtherUser){
                var obj = {};
                prom.push(obj.user = eachOtherUser.user);
                prom.push(obj.lat = eachOtherUser.latitude);
                prom.push(obj.long = eachOtherUser.longitude);

                prom.push(
                    userInfo.related(eachOtherUser.user).then(function(response) {
                        obj.info = response;
                    })
                );

               prom.push(near_users.push(obj));
            });

            $q.all(prom).then(function(){
                mapSetup(near_users);
            });
        };

        $scope.goToProfile = function(event, username) {
            event.preventDefault();
            window.location = location.origin + '/user/'+ username
        };



        //when dragon is ready start the magic for the page
        $dragon.onReady(function() {
            $scope.order = '-total';
            subscribeToChannels();
            Setup();

            $scope.$watch('nearUsers', function(newData){
                if(newData)
                    relatedData()
            });

            $dragon.onChannelMessage(function(channels, message) {
                $dragon.getList('locationcurrent', {latitude:$scope.myLocation.G,longitude: $scope.myLocation.K, user: user}).then(function(response){
                    $scope.nearUsers = response.data;
                });
            });
        });

});