import api from "./api";

export const verifyPAN = async (panNumber) => {
  const response = await api.post("/pan/verify", { pan_number: panNumber });
  return response.data;
};
