import React from "react";
import { Link } from "react-router-dom";

const FailurePage = () => {
  return (
    <div>
      <h1>Verification Failed</h1>
      <Link to="/">Retry</Link>
    </div>
  );
};

export default FailurePage;
