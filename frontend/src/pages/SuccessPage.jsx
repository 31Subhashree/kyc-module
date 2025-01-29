import React from "react";
import { Link } from "react-router-dom";

const SuccessPage = () => {
  return (
    <div>
      <h1>Verification Successful!</h1>
      <Link to="/">Go to Home</Link>
    </div>
  );
};

export default SuccessPage;
