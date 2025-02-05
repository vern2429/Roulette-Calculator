const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
app.use(bodyParser.json());

const API_KEY = "91fjl06tqnangipkbihqmlfjlpaptktycpx03hhmxupyyctusn3wcwiwy3bzuhj9";

// Approve payment
app.post("/approve-payment", async (req, res) => {
    const { paymentId } = req.body;
    try {
        await axios.post(`https://api.minepi.com/v2/payments/${paymentId}/approve`, {}, {
            headers: { Authorization: `Bearer ${API_KEY}` }
        });
        res.status(200).send("Payment approved");
    } catch (error) {
        console.error("Error approving payment:", error.message);
        res.status(500).send("Error approving payment");
    }
});

// Complete payment
app.post("/complete-payment", async (req, res) => {
    const { paymentId, txid } = req.body;
    try {
        await axios.post(`https://api.minepi.com/v2/payments/${paymentId}/complete`, { txid }, {
            headers: { Authorization: `Bearer ${API_KEY}` }
        });
        res.status(200).send("Payment completed");
    } catch (error) {
        console.error("Error completing payment:", error.message);
        res.status(500).send("Error completing payment");
    }
});

// Start server
const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
                      
