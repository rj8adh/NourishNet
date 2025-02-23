import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // Import navigation hook
import axios from "axios";
import "./Chatbot.css"; // Import the external CSS file

const Chatbot = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const chatContainerRef = useRef(null);
  const navigate = useNavigate(); // Hook for navigation

  const OPENAI_API_KEY = import.meta.env.VITE_OPENAI_API_KEY;
  const NUTRITIONIX_APP_ID = import.meta.env.VITE_NUTRITIONIX_APP_ID; 
  const NUTRITIONIX_APP_KEY = import.meta.env.VITE_NUTRITIONIX_APP_KEY; 

  useEffect(() => {
    chatContainerRef.current?.scrollTo({ top: chatContainerRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const fetchNutritionData = async (query) => {
    try {
      const response = await axios.get(`https://api.nutritionix.com/v1_1/search/${query}`, {
        params: {
          appId: NUTRITIONIX_APP_ID,
          appKey: NUTRITIONIX_APP_KEY,
          fields: "item_name,nf_calories,nf_protein,nf_total_fat,nf_total_carbohydrate",
        },
      });

      if (response.data.hits.length > 0) {
        const food = response.data.hits[0].fields;
        return `🍏 **${food.item_name.toUpperCase()}** 🍏\nCalories: ${food.nf_calories} kcal\nProtein: ${food.nf_protein}g\nFat: ${food.nf_total_fat}g\nCarbs: ${food.nf_total_carbohydrate}g`;
      }
    } catch (error) {
      console.error("Error fetching nutrition data:", error);
    }
    return null;
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { role: "user", content: input };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setInput("");

    const nutritionResponse = await fetchNutritionData(input);
    if (nutritionResponse) {
      setMessages((prevMessages) => [...prevMessages, { role: "bot", content: nutritionResponse }]);
      return;
    }

    try {
      const response = await axios.post(
        "https://api.openai.com/v1/chat/completions",
        {
          model: "gpt-3.5-turbo",
          messages: [...messages, newMessage],
        },
        {
          headers: {
            Authorization: `Bearer ${OPENAI_API_KEY}`,
            "Content-Type": "application/json",
          },
        }
      );

      const botReply = response.data.choices[0]?.message;
      if (botReply) {
        setMessages((prevMessages) => [...prevMessages, botReply]);
      }
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  return (
    <div className="chat-container">
      <h2 className="chat-title">🍎 Food Nutrition Chatbot 🥦</h2>

      <div ref={chatContainerRef} className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-message-container ${msg.role === "user" ? "user-container" : "bot-container"}`}>
            <div className={`chat-message ${msg.role === "user" ? "chat-user" : "chat-bot"}`}>
              {msg.content}
            </div>
          </div>
        ))}
      </div>

      <div className="chat-input-container">
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button className="chat-send-button" onClick={sendMessage}>🡅</button>
      </div>

      {/* Back to Home Button */}
      <button className="back-button" onClick={() => navigate("/")}>
        ⬅ Back to Home
      </button>
    </div>
  );
};

export default Chatbot;
