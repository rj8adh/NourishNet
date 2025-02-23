import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Results = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const recipes = location.state?.recipes;

    if (!recipes) {
        return <div>No recipes found.</div>;
    }

    const handleImageClick = (index) => {
        navigate(`/recipe/${index}`, { state: { recipes: recipes } });
    };

    return (
        <div>
            <h1>Recipe Results</h1>
            {recipes.map((recipe, index) => (
                <div key={recipe.id}>
                    <h2>{recipe.title}</h2>
                    <img
                        src={recipe.image}
                        alt={recipe.title}
                        onClick={() => handleImageClick(index)}
                        style={{ cursor: 'pointer' }}
                    />
                </div>
            ))}
        </div>
    );
};

export default Results;