import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PANVerification from "./pages/PANVerification";
import BankVerification from "./pages/BankVerification";
import SuccessPage from "./pages/SuccessPage";
import FailurePage from "./pages/FailurePage";
import Navbar from "./components/Navbar";
import "./styles.css";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<PANVerification />} />
        <Route path="/bank-verification" element={<BankVerification />} />
        <Route path="/success" element={<SuccessPage />} />
        <Route path="/failure" element={<FailurePage />} />
      </Routes>
    </Router>
  );
};

export default App;
