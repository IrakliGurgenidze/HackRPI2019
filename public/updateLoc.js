


function updateBack(data) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/locationUpdate", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
      console.log("ok");
    } 
  }
  xhr.send(JSON.stringify(data));   
}

const goog_url = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAyvffxPyhhnkmN_t19LwRlJ-KErJWiNHY";

function goog_loc() {
  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      data = JSON.parse(xhr.response);
      console.log(data);
      updateBack(data);
    }
  }
  xhr.open("POST", goog_url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send();
}
