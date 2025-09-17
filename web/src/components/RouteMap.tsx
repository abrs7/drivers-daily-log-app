import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet";
import { LatLngExpression } from "leaflet";

interface RouteMapProps {
  geometry: {
    coordinates: [number, number][];
  };
}

export function RouteMap({ geometry }: RouteMapProps) {
  if (!geometry) return <p>No route available</p>;

  const positions: LatLngExpression[] = geometry.coordinates.map(
    ([lon, lat]) => [lat, lon] // leaflet needs [lat, lon]
  );

  return (
    <MapContainer
      center={positions[0] as LatLngExpression}
      zoom={6}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      <Polyline positions={positions} color="blue" />
      <Marker position={positions[0]}>
        <Popup>Start</Popup>
      </Marker>
      <Marker position={positions[positions.length - 1]}>
        <Popup>End</Popup>
      </Marker>
    </MapContainer>
  );
}
