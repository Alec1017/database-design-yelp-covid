//import './App.css';
import 'leaflet/dist/leaflet.css';
import {MapContainer, TileLayer, Marker, Circle} from 'react-leaflet';
import {icon} from 'leaflet';
import { closedBusinessData, collegeData, bostonLocations } from "./data.js";

function App() {

  var myIcon = icon({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
    iconSize: [20, 40],
    iconAnchor: [22, 50],
    popupAnchor: [-3, -76],
});


  return (
    <div className="App">
      <MapContainer center={[42.3601, -71.0589]} zoom={13} scrollWheelZoom={false} style={{height: '100vh', width: '100%'}}>
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {closedBusinessData.map((value, index) => {
          return <Marker 
                    position={[value['latitude'], value['longitude']]} 
                    icon={myIcon}
                 />
        })}

        {/* {collegeData.map((value, index) => {
          return <Circle center={[value['latitude'], value['longitude']]} pathOptions={{color: 'red'}} radius={1000} />
        })} */}
        {bostonLocations.map((value, index) => {
          return <Circle center={[value['latitude'], value['longitude']]} pathOptions={{color: 'blue'}} radius={1100} />
        })}
      </MapContainer>
    </div>
  );
}

export default App;
