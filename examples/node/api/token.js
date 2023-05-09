const path = require("path");
require("dotenv").config({ path: path.resolve(__dirname, "../.env.local") });
const axios = require("axios");

const handler = async (req, res) => {
  if (req.method === "POST") {
    const { code, wallet_signature } = req.body;

    const auth = Buffer.from(
      `${process.env.CLIENT_ID}:${process.env.CLIENT_SECRET}`
    ).toString("base64");

    const headers = {
      Authorization: `Basic ${auth}`,
    };

    const data = {
      code: code,
      grant_type: "https://gamium.world/oauth/grant_types/connectwallet",
      wallet_signature: wallet_signature,
    };

    try {
      const token_response = await axios.post(
        process.env.API_URL + "token/",
        data,
        { headers }
      );
      res.status(token_response.status).json(token_response.data);
    } catch (error) {
      const errorData = error.response?.data || { message: error.message };
      res.status(error.response?.status || 500).json(errorData);
    }
  } else {
    res.setHeader("Allow", "POST");
    res.status(405).end("Method Not Allowed");
  }
};

module.exports = handler;
