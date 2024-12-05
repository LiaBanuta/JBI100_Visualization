import React, { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';

// Replace with your actual Mapbox token
mapboxgl.accessToken = 'pk.eyJ1IjoidmRhdHR3YW5pIiwiYSI6ImNtNGIxMjMweTBiMTUybHF6aDZxcmJiMmkifQ.nDUHRcoFLFh2j1SG0s2KTw';

const MapView = ({ data, selectedYear, selectedState }) => {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const markers = useRef([]);

  // Initialize the map
  useEffect(() => {
    if (map.current) return;

    try {
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [133.7751, -25.2744], // Center of Australia
        zoom: 3
      });

      map.current.addControl(new mapboxgl.NavigationControl());
    } catch (error) {
      console.error('Error initializing map:', error);
    }
  }, []);

  // Update markers when data or filters change
  useEffect(() => {
    if (!map.current || !data) return;

    // Remove existing markers
    markers.current.forEach(marker => marker.remove());
    markers.current = [];

    try {
      // Filter incidents based on selected year and state
      const filteredIncidents = Array.isArray(data) ? data.filter(incident => {
        const yearMatch = selectedYear === 'all' || incident['Incident.year'].toString() === selectedYear;
        const stateMatch = selectedState === 'all' || incident.State === selectedState;
        return yearMatch && stateMatch;
      }) : [];

      console.log('Filtered incidents:', filteredIncidents.length);

      // Add markers for filtered incidents
      filteredIncidents.forEach(incident => {
        if (incident.Latitude && incident.Longitude) {
          const el = document.createElement('div');
          el.className = 'marker';

          const popupContent = `
            <div class="popup-content">
              <h3 style="font-weight: bold; margin-bottom: 8px; color: white;">
                ${incident.Location || 'Unknown Location'}
              </h3>
              <p style="margin: 4px 0; color: #e5e7eb;">
                <strong>Year:</strong> ${incident['Incident.year']}
              </p>
              <p style="margin: 4px 0; color: #e5e7eb;">
                <strong>Activity:</strong> ${incident['Victim.activity'] || 'Unknown'}
              </p>
              <p style="margin: 4px 0; color: #e5e7eb;">
                <strong>State:</strong> ${incident.State}
              </p>
              ${incident['Victim.injury'] ? 
                `<p style="margin: 4px 0; color: #e5e7eb;">
                  <strong>Injury:</strong> ${incident['Victim.injury']}
                </p>` : ''
              }
            </div>
          `;

          const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(popupContent);

          const marker = new mapboxgl.Marker(el)
            .setLngLat([incident.Longitude, incident.Latitude])
            .setPopup(popup)
            .addTo(map.current);

          // Fix accessibility for the popup close button
          popup.on('open', () => {
            const closeButton = popup._container.querySelector('.mapboxgl-popup-close-button');
            if (closeButton) {
              closeButton.removeAttribute('aria-hidden');
              closeButton.setAttribute('aria-label', 'Close popup');
            }
          });

          markers.current.push(marker);
        }
      });

      // Fit map to markers if there are any
      if (filteredIncidents.length > 0) {
        const bounds = new mapboxgl.LngLatBounds();
        filteredIncidents.forEach(incident => {
          if (incident.Latitude && incident.Longitude) {
            bounds.extend([incident.Longitude, incident.Latitude]);
          }
        });

        map.current.fitBounds(bounds, {
          padding: 50,
          maxZoom: 12
        });
      }
    } catch (error) {
      console.error('Error updating markers:', error);
    }
  }, [data, selectedYear, selectedState]);

  return (
    <div
      ref={mapContainer}
      className="map-container"
      style={{ width: '100%', height: '100%', borderRadius: '0.5rem' }}
    />
  );
};

export default MapView;
