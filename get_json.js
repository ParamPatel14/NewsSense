// const request = require("request");
// const path = require("path");
// const fs=require("fs");
// require('dotenv').config();
// const apiKey=process.env.API_KEY

// let symbol='IBM'
// let intervel ='5min'
// const url=`https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=B335UBK5AAWH4E9Y`;

// let json_data = null;
// const filePath = path.join("C:", "Users", "spune", "Desktop", "NewsSense", "stock_data.json");
// request.get({
//     url: url,
//     json: true,
//     headers: {'User-Agent': 'request'}
//   }, (err, res, data) => {
//     if (err) {
//       console.log('Error:', err);
//       console.log("abc");
//     } else if (res.statusCode !== 200) {
//       console.log('Status:', res.statusCode);
//       console.log("def")
//     } else {
//       //writing to external json file
//       saveJsonToFile(data,filePath)
//     }
// });

// async function saveJsonToFile(data, filePath) {
//         try {
//           const jsonString = JSON.stringify(data, null, 2);
//           await fs.promises.writeFile(filePath, jsonString, 'utf8'); // ✅ Using promises
//           console.log(`Successfully saved JSON data to: ${filePath}`);
//         } catch (error) {
//           console.error(`Error saving JSON data to file ${filePath}:`, error);
//         }
//     }


const path = require("path");
const fs = require("fs");
require("dotenv").config();

const apiKey = process.env.API_KEY;
const symbol = "IBM";
const interval = "5min";

const url = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=${apiKey}`;
// Set your desired file path
const filePath = path.join(require("os").homedir(), "Desktop", "NewsSense", "stock_data.json");

async function fetchStockData() {
  try {
    const response = await fetch(url, {
      headers: { "User-Agent": "fetch" },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    await saveJsonToFile(data, filePath);
  } catch (error) {
    console.error("Error fetching stock data:", error);
  }
}

async function saveJsonToFile(data, filePath) {
  try {
    const jsonString = JSON.stringify(data, null, 2);
    await fs.promises.writeFile(filePath, jsonString, "utf8");
    console.log(`Successfully saved JSON data to: ${filePath}`);
  } catch (error) {
    console.error(`Error saving JSON data to file ${filePath}:`, error);
  }
}

fetchStockData();
