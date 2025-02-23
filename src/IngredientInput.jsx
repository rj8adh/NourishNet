import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./IngredientInput.css"; // Import the CSS file

const IngredientInput = () => {
  const [ingredient, setIngredient] = useState("");
  const [ingredients, setIngredients] = useState(
    JSON.parse(localStorage.getItem("ingredients")) || []
  );
  const navigate = useNavigate(); // Hook to navigate

  // Add ingredient
  const addIngredient = () => {
    if (ingredient.trim()) {
      const updatedIngredients = [...ingredients, ingredient.trim()];
      setIngredients(updatedIngredients);
      localStorage.setItem("ingredients", JSON.stringify(updatedIngredients));
      setIngredient(""); // Clear input
    }
  };

  // Remove ingredient
  const removeIngredient = (index) => {
    const updatedIngredients = ingredients.filter((_, i) => i !== index);
    setIngredients(updatedIngredients);
    localStorage.setItem("ingredients", JSON.stringify(updatedIngredients));
  };

  return (
    <div className="ingredient-container">
      <h2>Enter Ingredients</h2>

      {/* Input Field and Add Button */}
      <div className="input-group">
        <input
          type="text"
          value={ingredient}
          onChange={(e) => setIngredient(e.target.value)}
          placeholder="Add an ingredient"
        />
        <button onClick={addIngredient}>Add</button>
      </div>

      {/* Ingredient List */}
      <div className="ingredient-list">
        {ingredients.map((item, index) => (
          <div key={index} className="ingredient-item">
            {item}
            <button className="remove-button" onClick={() => removeIngredient(index)}>×</button>
          </div>
        ))}
      </div>

      {/* Back to Home Button */}
      <div className="button-container">
        <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      </div>
    </div>
  );
};

export default IngredientInput;
