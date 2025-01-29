import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyBank } from "../services/bankService";

const BankVerification = () => {
  const [accountNumber, setAccountNumber] = useState("");
  const [ifscCode, setIFSCCode] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await verifyBank(accountNumber, ifscCode);
      if (response.status === "success") {
        navigate("/success");
      } else {
        setError("Bank account verification failed.");
      }
    } catch (err) {
      setError("An error occurred during verification.");
    }
  };

  return (
    <div>
      <h1>Bank Account Verification</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Account Number"
          value={accountNumber}
          onChange={(e) => setAccountNumber(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Enter IFSC Code"
          value={ifscCode}
          onChange={(e) => setIFSCCode(e.target.value)}
          required
        />
        <button type="submit">Verify</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default BankVerification;
