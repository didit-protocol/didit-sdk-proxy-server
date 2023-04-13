const path = require('path')
require('dotenv').config({ path: path.resolve(__dirname, '../.env.local') })
const axios = require("axios");

const handler = async (req, res) => {
  if (req.method === "POST") {
    const { scope, wallet_address, claims } = req.body;

    const auth = Buffer.from(`${process.env.CLIENT_ID}:${process.env.CLIENT_SECRET}`).toString("base64");

    const headers = {
      "Content-Type": "application/json",
      "Authorization": `Basic ${auth}`,
    };

    const data = {};
    if (scope) data["scope"] = scope;
    if (wallet_address) data["wallet_address"] = wallet_address;
    if (claims) data["claims"] = claims;

    try {
        const wallet_authorization_response = await axios.post(process.env.API_URL + "wallet_authorization/", data, { headers });
        res.status(wallet_authorization_response.status).json(wallet_authorization_response.data);
      } catch (error) {
        const errorData = error.response?.data || { message: error.message };
        res.status(error.response?.status || 500).json(errorData);
      }
  } else {
    res.setHeader("Allow", "POST");
    res.status(405).end("Method Not Allowed lol");
  }
};

module.exports = handler;