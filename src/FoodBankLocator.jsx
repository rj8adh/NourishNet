import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./FoodBankLocator.css";

const FoodBankLocator = () => {
  const [zip, setZip] = useState("");
  const [foodBanks, setFoodBanks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const GOOGLE_API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;

  console.log("Google API Key:", GOOGLE_API_KEY);

  const findFoodBanks = async () => {
    if (!zip.trim()) {
      setError("Please enter a valid zip code.");
      return;
    }

    setLoading(true);
    setError("");
    setFoodBanks([]);

    try {
      // Debugging: Log API key
      console.log("Using Google API Key:", GOOGLE_API_KEY);

      // Step 1: Get Lat/Lng from Zip Code
      const geoResponse = await axios.get(
        `https://maps.googleapis.com/maps/api/geocode/json`,
        { params: { address: zip, key: GOOGLE_API_KEY } }
      );

      console.log("Geocode Response:", geoResponse.data);

      if (!geoResponse.data.results.length) {
        throw new Error("Invalid zip code or no results found.");
      }

      const location = geoResponse.data.results[0]?.geometry.location;
      if (!location) throw new Error("Invalid zip code.");

      // Step 2: Find Nearby Food Banks
      const placesResponse = await axios.get(
        `https://maps.googleapis.com/maps/api/place/nearbysearch/json`,
        {
          params: {
            location: `${location.lat},${location.lng}`,
            radius: 10000,
            type: "food_bank",
            key: GOOGLE_API_KEY,
          },
        }
      );

      console.log("Places API Response:", placesResponse.data);

      if (!placesResponse.data.results.length) {
        throw new Error("No food banks found in your area.");
      }

      let places = placesResponse.data.results.slice(0, 5);

      // Step 3: Fetch Details for Each Food Bank
      const detailsPromises = places.map(async (place) => {
        const detailsResponse = await axios.get(
          `https://maps.googleapis.com/maps/api/place/details/json`,
          {
            params: {
              place_id: place.place_id,
              fields: "name,formatted_address,formatted_phone_number,website",
              key: GOOGLE_API_KEY,
            },
          }
        );
        return detailsResponse.data.result;
      });

      const details = await Promise.all(detailsPromises);
      setFoodBanks(details);
    } catch (err) {
      console.error("Error:", err);
      setError(err.message || "Failed to fetch food banks. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="food-bank-container">
      <h2>Find Nearby Food Banks</h2>
      <input
        type="text"
        placeholder="Enter Zip Code"
        value={zip}
        onChange={(e) => setZip(e.target.value)}
        className="zip-input"
      />
      <button onClick={findFoodBanks} className="search-button">Search</button>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      <ul className="food-bank-list">
        {foodBanks.map((bank, i) => (
          <li key={i} className="food-bank">
            <h3>{bank.name}</h3>
            <p><strong>Address:</strong> {bank.formatted_address}</p>
            <p><strong>Phone:</strong> {bank.formatted_phone_number || "N/A"}</p>
            <p>
              <strong>Website:</strong>{" "}
              {bank.website ? (
                <a href={bank.website} target="_blank" rel="noopener noreferrer">
                  {bank.website}
                </a>
              ) : (
                "N/A"
              )}
            </p>
          </li>
        ))}
      </ul>

      <button className="home-button" onClick={() => navigate("/")}>
        Return Home
      </button>
    </div>
  );
};

export default FoodBankLocator;
