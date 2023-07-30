angular.module('mediabro', ['shagstrom.angular-split-pane'])
.controller('MainCtrl', function ($scope) {
    $scope.splitPaneProperties = {};

    $scope.setFirstComponent = function (value) {
        $scope.splitPaneProperties.firstComponentSize = value;
    };
    $scope.setLastComponent = function (value) {
        console.log(value);
        $scope.splitPaneProperties.lastComponentSize = value;
    };

    // playback speed options
    $scope.options = [];

    for (var i = 50; i <= 200; i += 10) {
        var n = i / 100;
        $scope.options.push({name: n + 'x', value: n});
    }

    $scope.data = {currentSpeed: $scope.options[5].value};

    $scope.setPlaybackRate = function (item) {
        console.log('playbackSpeed', item.data.currentSpeed);

        if(audioplayer.is(':visible')) {
            audioplayer[0].playbackRate = item.data.currentSpeed;
        } else if(videoplayer.is(':visible')) {
            videoplayer[0].playbackRate = item.data.currentSpeed;
        } else {
            $scope.data = {currentSpeed: $scope.options[5].value};
        }
    }
});