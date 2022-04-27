
function findplace()
{

    place = document.getElementById('placename');
    loc = document.getElementById('location');
    place = place.value;
    loc = loc.value;
    document.getElementById('placename').value = "";
    document.getElementById('location').value = "";


    address = place +" ," + loc;
    codeAddress(address);

   var clustringnodelist = [] , clusteringcenterlist = [];
   let url1=new URL( "http://localhost:8000/havershine")
   url1.searchParams.append('location',loc)
    fetch(url1)
    .then(response => response.json())
    .then(data => {
        data = JSON.parse(data);
        // rentallocationlist = [];
        // amenditiesmarekr = [];
        // deleteamenditiesMarkers();
        // deleterentalMarkers();
        // for(var i=0;i<data.length;i++)
        // {
        //     if(data[i].length > 7)
        //     {
        //         rentallocationlist.push(data[i]);  
        //     }
        //     else
        //     {
        //         let marker = new google.maps.Marker(
        //             {
        //                 map: map,
        //                 position: {lat:data[i][1] , lng:data[i][2]},
        //                 title : String(data[i][5]),
        //                 opacity : 0.7,
        //                 icon: "assets/markers/" + String(data[i][6]) +".png"
        //             });
        //             amenditiesmarekr.push(marker);
        //     }
        // }
        // finddistance();
        // setamenditiesmarker(map)
    });   


}





function initMap()
{
    var location = {lat:19.418864 , lng:72.815619};
    map = new google.maps.Map(document.getElementById("map") , {
        zoom:13, 
        center : location
    });
    var marker = new google.maps.Marker({
        position : location ,
        map: map
    });
    markers.push(marker);
    setMapOnAll(map);
    geocoder = new google.maps.Geocoder();  
    directionsRenderer.setMap(map);  
}