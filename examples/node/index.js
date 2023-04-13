const express = require('express');
const cors = require('cors');
const walletAuthorizationHandler = require('./api/wallet_authorization');
const tokenHandler = require('./api/token');

const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.urlencoded({ extended: true }));

app.post('/wallet_authorization', walletAuthorizationHandler);
app.post('/token', tokenHandler);  

app.listen(port, () => {
  console.log(`Backend server listening on port ${port}`);
});