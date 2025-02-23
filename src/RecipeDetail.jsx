import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const RecipeDetail = () => {
    const { recipeId } = useParams();
    const [missing, setMissing] = useState(null);
    const [equip, setEquip] = useState(null);
    const [step, setStep] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchAll = async () => {
            setLoading(true);
            setError(null);
            try {
                const missingResponse = await fetch('/getMissingIngredients');
                const missingData = await missingResponse.json();
                setMissing(missingData[recipeId]);

                const equipResponse = await fetch('/getNecessaryEquipment');
                const equipData = await equipResponse.json();
                setEquip(equipData[recipeId]);

                const stepsResponse = await fetch('/getIngredientSteps');
                const stepsData = await stepsResponse.json();
                setStep(stepsData[recipeId]);

            } catch (error) {
                setError("Failed to load recipe details.");
                console.error("API Call Error:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchAll();
    }, [recipeId]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!missing && !equip && !step) {
        return <div>Recipe details not found.</div>;
    }

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f0f8ff' }}> {/* Added background color */}
            <h1 style={{ marginBottom: '20px' }}>Recipe Details</h1>

            {missing && missing.length > 0 && (
                <div style={{ marginBottom: '20px', backgroundColor: '#e0ffff', padding: '10px', borderRadius: '5px' }}> {/* Added background color to each section */}
                    <h2>Missing Ingredients:</h2>
                    <ul style={{ listStyleType: 'disc', marginLeft: '20px' }}>
                        {missing.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </div>
            )}

            {equip && equip.length > 0 && (
                <div style={{ marginBottom: '20px', backgroundColor: '#f0e68c', padding: '10px', borderRadius: '5px' }}> {/* Added background color to each section */}
                    <h2>Equipment:</h2>
                    <ul style={{ listStyleType: 'disc', marginLeft: '20px' }}>
                        {equip.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </div>
            )}

            {step && step.length > 0 && (
                <div style={{ marginBottom: '20px', backgroundColor: '#98fb98', padding: '10px', borderRadius: '5px' }}> {/* Added background color to each section */}
                    <h2>Steps:</h2>
                    <p style={{ whiteSpace: 'pre-line' }}>{step}</p>
                </div>
            )}

            {(!missing || missing.length === 0) && (!equip || equip.length === 0) && (!step || step.length === 0) && (
                <div>No details available for this recipe.</div>
            )}
        </div>
    );
};

export default RecipeDetail;