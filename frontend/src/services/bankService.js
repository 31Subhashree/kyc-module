import api from "./api";

export const verifyBank = async (accountNumber, ifscCode) => {
  const response = await api.post("/bank/verify", {
    account_number: accountNumber,
    ifsc_code: ifscCode,
  });
  return response.data;
};
