import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./IngredientInput.css";

const IngredientInput = () => {
  const [ingredient, setIngredient] = useState("");
  const [ingredients, setIngredients] = useState(
    JSON.parse(localStorage.getItem("ingredients")) || []
  );
  const navigate = useNavigate();

  const addIngredient = () => {
    if (ingredient.trim()) {
      const updatedIngredients = [...ingredients, ingredient.trim()];
      setIngredients(updatedIngredients);
      localStorage.setItem("ingredients", JSON.stringify(updatedIngredients));
      setIngredient("");
    }
  };

  const removeIngredient = (index) => {
    const updatedIngredients = ingredients.filter((_, i) => i !== index);
    setIngredients(updatedIngredients);
    localStorage.setItem("ingredients", JSON.stringify(updatedIngredients));
  };

  const handleSubmit = async () => {
    console.log("handleSubmit called");
    const ingredientsString = ingredients.join("&");

    try {
      const response = await fetch("/giveIngredients", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ingredients: ingredientsString }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      navigate("/results", { state: { recipes: data } });
    } catch (error) {
      console.error("Error sending ingredients:", error);
      // Handle error display to the user
    }
  };

  return (
    <div className="ingredient-container">
      <h2>Enter Ingredients</h2>

      <div className="input-group">
        <input
          type="text"
          value={ingredient}
          onChange={(e) => setIngredient(e.target.value)}
          placeholder="Add an ingredient"
        />
        <button onClick={addIngredient}>Add</button>
      </div>

      <div className="ingredient-list">
        {ingredients.map((item, index) => (
          <div key={index} className="ingredient-item">
            {item}
            <button className="remove-button" onClick={() => removeIngredient(index)}>
              ×
            </button>
          </div>
        ))}
      </div>

      <div className="button-container">
        <button className="submit-button" onClick={handleSubmit}>
          Submit
        </button>
      </div>

      <div className="button-container">
        <button className="back-button" onClick={() => navigate("/")}>
          Back to Home
        </button>
      </div>
    </div>
  );
};

export default IngredientInput;