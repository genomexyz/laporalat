<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>PETA STATUS PERALATAN DI BANDARA</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">


    <!-- Custom fonts for this template -->
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css">
    <link href='https://fonts.googleapis.com/css?family=Kaushan+Script' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Droid+Serif:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.4.0/dist/leaflet.css" integrity="sha512-puBpdR0798OZvTTbP4A8Ix/l+A4dHDD0DGqYW6RQ+9jxkRFclaxxQb/SJAWZfWAkuyeQUytO7+7N4QKrDh+drA==" crossorigin=""/>


  </head>

  <body id="page-top">


    <section class="bg-light" id="produk" style="padding-bottom:20px;">
		<div class="container">
			<div class="row">
				<h3>PETA STATUS PERALATAN DI BANDARA</h3>
			</div>
			<div class="row">
				<div id="map" style="width:1200px;height:700px;"></div>
			</div>
			<div class="row">
				<div id="map" style="width:1200px;height:700px;">
				</div>
			</div>
		</div>	
	</section>



<!-- Bootstrap core JavaScript -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>


    <script src="https://unpkg.com/leaflet@1.4.0/dist/leaflet.js" integrity="sha512-QVftwZFqvtRNi0ZyCtsznlKSWOStnDORoefr1enyq5mVL4tmKB3S/EnC3rRJcxCPavG10IcrVGSmPh6Qw5lwrg==" crossorigin=""></script>

    
	<!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"> -->

</body>

<script>

//setting
bandaranama = []
bandaramarker = []
bandaralat = []
bandaralon = []
bandaraawosANEMOMETER = []
bandaraawosBAROMETER = []
bandaraawosTERMOMETER = []
bandaraawosCEILOMETER = []
bandaraawosVISIBILITY = []
bandararadar = []
bandarallwas = []
bandaralidarva = []

function loadbandara() {
	var nama = []
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		alldata = this.responseText.split("\n");
		for (i = 0; i < alldata.length; i++) {
			var temp = alldata[i].split(",");
			if (temp == "") {
				continue;
			}
			//console.log(temp);
			bandaranama.push(temp[0]);
			bandaralat.push(parseFloat(temp[1]));
			bandaralon.push(parseFloat(temp[2]));
			bandaraawosANEMOMETER.push(temp[3]);
			bandaraawosBAROMETER.push(temp[4]);
			bandaraawosTERMOMETER.push(temp[5]);
			bandaraawosCEILOMETER.push(temp[6]);
			bandaraawosVISIBILITY.push(temp[7]);
			bandararadar.push(temp[8]);
			bandarallwas.push(temp[9]);
			bandaralidarva.push(temp[10]);
		}
    }
  };
  xhttp.open("GET", "mapdb.csv", false);
  xhttp.send();
}



var sudahlapor = L.layerGroup();
var ICONmarker = L.icon({
    iconUrl: 'icon.png',

	iconSize:     [15, 15], // size of the icon
	iconAnchor:   [8, 8], // point of the icon which will correspond to marker's location
	popupAnchor:  [6, 0] // point from which the popup should open relative to the iconAnchor
});

var belumlapor = L.layerGroup();
var ICONmarkerBELUMLAPOR = L.icon({
    iconUrl: 'icon-belumlapor.png',

	iconSize:     [15, 15], // size of the icon
	iconAnchor:   [8, 8], // point of the icon which will correspond to marker's location
	popupAnchor:  [6, 0] // point from which the popup should open relative to the iconAnchor
});


loadbandara();
console.log(bandaranama.length);
for (i = 0; i < bandaranama.length; i++) {
	if (bandaraawosANEMOMETER[i] == 'belum lapor') {
		bandaramarker.push(L.marker([bandaralat[i], bandaralon[i]], {icon: ICONmarkerBELUMLAPOR}));
		bandaramarker[i].addTo(belumlapor);
	} else {
		bandaramarker.push(L.marker([bandaralat[i], bandaralon[i]], {icon: ICONmarker}));
		bandaramarker[i].addTo(sudahlapor);
	}
	bandaramarker[i].bindPopup("<b>"+bandaranama[i]+"</b>"+"<br>"+
	"keterangan:<br>"+
	"<ul>"+
	"<li>(AWOS) Anemometer: "+bandaraawosANEMOMETER[i]+"</li>"+
	"<li>(AWOS) Barometer: "+bandaraawosBAROMETER[i]+"</li>"+
	"<li>(AWOS) Termometer: "+bandaraawosTERMOMETER[i]+"</li>"+
	"<li>(AWOS) Ceilometer: "+bandaraawosCEILOMETER[i]+"</li>"+
	"<li>(AWOS) Visibility: "+bandaraawosVISIBILITY[i]+"</li>"+
	"<li>RADAR: "+bandararadar[i]+"</li>"+
	"<li>LLWAS: "+bandarallwas[i]+"</li>"+
	"<li>LIDAR VA: "+bandaralidarva[i]+"</li>"+
	"</ul>");
}


var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

var grayscale   = L.tileLayer(mbUrl, {id: 'mapbox.light', attribution: mbAttr}),
	streets  = L.tileLayer(mbUrl, {id: 'mapbox.streets',   attribution: mbAttr});

var map = L.map('map', {
		center: [0, 120],
		zoom: 5,
		layers: [streets, sudahlapor, belumlapor]
});

var baseLayers = {
	"Grayscale": grayscale,
	"Streets": streets
};

var overlays = {
	"<span style='color:green'>Stasiun yang sudah lapor peralatannya hari ini</span>": sudahlapor,
	"<span style='color:red'>Stasiun yang belum lapor peralatannya hari ini</span>": belumlapor
};

L.control.layers(baseLayers, overlays).addTo(map);


</script>

</html>
