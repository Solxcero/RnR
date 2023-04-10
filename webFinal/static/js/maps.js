var map = new kakao.maps.Map(document.getElementById('map'), { // 지도를 표시할 div
    center : new kakao.maps.LatLng(37.52412930882497, 126.9223842345341), // 지도의 중심좌표 
    level : 10 // 지도의 확대 레벨 
});

// 마커 클러스터러를 생성합니다 
var clusterer = new kakao.maps.MarkerClusterer({
    map: map, // 마커들을 클러스터로 관리하고 표시할 지도 객체 
    averageCenter: true, // 클러스터에 포함된 마커들의 평균 위치를 클러스터 마커 위치로 설정 
    minLevel: 10 // 클러스터 할 최소 지도 레벨 
});


$.get("hotel.json", function(data) {
    var markers = $(data).map(function(i, hotel) {
        var marker = new kakao.maps.Marker({
            position: new kakao.maps.LatLng(hotel.latitude, hotel.longitude),
            title: hotel.ht_name // 호텔 이름 정보를 마커의 title
        });

        // 인포윈도우를 생성합니다
        var infowindow = new kakao.maps.InfoWindow({
            content: '<div style="padding:5px;">' + hotel.ht_name + '</div>', // 인포윈도우에 표시할 내용
            removable: true // 인포윈도우를 닫을 수 있는 x 버튼 표시
        });

        // 마커를 클릭했을 때, 인포윈도우를 토글합니다
        kakao.maps.event.addListener(marker, 'click', function() {
            if (infowindow.getMap()) {
                infowindow.close();
            } else {
                infowindow.open(map, marker);
            }
        });

        return marker;
    });

    // 클러스터러에 마커들을 추가합니다
    clusterer.addMarkers(markers);
});