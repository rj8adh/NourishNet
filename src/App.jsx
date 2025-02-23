import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Chatbot from "./Chatbot";
import FoodBankLocator from "./FoodBankLocator";
import "./App.css";

function Home() {
  return (
    <div className="home-container">
      <h1>Welcome to NourishNet</h1>
      <div className="button-container">
        <Link to="/chatbot">
          <button className="nav-button">Start Chat</button>
        </Link>
        <Link to="/foodbanks">
          <button className="nav-button">Find Food Banks</button>
        </Link>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/foodbanks" element={<FoodBankLocator />} />
      </Routes>
    </Router>
  );
}

export default App;
