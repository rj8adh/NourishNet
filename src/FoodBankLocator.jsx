import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./FoodBankLocator.css";

const FoodBankLocator = () => {
  const [zip, setZip] = useState("");
  const [foodBanks, setFoodBanks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const findFoodBanks = async () => {
    if (!zip.trim()) {
      setError("Please enter a valid zip code.");
      return;
    }

    setLoading(true);
    setError("");
    setFoodBanks([]);

    try {
      const response = await axios.get(`http://127.0.0.1:8000/foodbanks/${zip}`); // Use full URL
      console.log("Response Data:", response.data);
      setFoodBanks(response.data);
    } catch (err) {
      console.error("Error:", err);
      setError(err.response?.data?.detail || "Failed to fetch food banks. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log("FoodBanks in Render:", foodBanks);
  }, [foodBanks]);

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

      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p className="error">{error}</p>
      ) : Array.isArray(foodBanks) && foodBanks.length > 0 ? (
        <ul className="food-bank-list">
          {foodBanks.map((bank, i) => {
            console.log("bank number: " + i, bank);
            if (typeof bank === "object" && bank !== null) {
              return (
                <li key={i} className="food-bank">
                  <h3>{bank?.name || "Name not available"}</h3>
                  <p>
                    <strong>Address:</strong> {bank?.formatted_address || "Address not available"}
                  </p>
                  <p>
                    <strong>Phone:</strong> {bank?.formatted_phone_number || "N/A"}
                  </p>
                  <p>
                    <strong>Website:</strong>{" "}
                    {bank?.website ? (
                      <a href={bank.website} target="_blank" rel="noopener noreferrer">
                        {bank.website}
                      </a>
                    ) : (
                      "N/A"
                    )}
                  </p>
                </li>
              );
            } else {
              return <li key={i}>Invalid data</li>;
            }
          })}
        </ul>
      ) : (
        <p>
          {Array.isArray(foodBanks)
            ? "Please enter a zip code to search."
            : "Please enter a zip code to search."}
        </p>
      )}

      <button className="home-button" onClick={() => navigate("/")}>
        Return Home
      </button>
    </div>
  );
};

export default FoodBankLocator;