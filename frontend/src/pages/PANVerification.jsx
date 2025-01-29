import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyPAN } from "../services/panService";

const PANVerification = () => {
  const [pan, setPAN] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await verifyPAN(pan);
      if (response.status === "success") {
        navigate("/bank-verification");
      } else {
        setError("PAN verification failed.");
      }
    } catch (err) {
      setError("An error occurred during verification.");
    }
  };

  return (
    <div>
      <h1>PAN Verification</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter PAN"
          value={pan}
          onChange={(e) => setPAN(e.target.value)}
          required
        />
        <button type="submit">Verify</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default PANVerification;
