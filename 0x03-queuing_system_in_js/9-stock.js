#!/usr/bin/yarn dev
// Import necessary modules
import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

// Define an array of products with their details
const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4
  },
  // Add more product objects as needed...
];

// Function to retrieve product details by item ID
const getItemById = (id) => {
  const item = listProducts.find(obj => obj.itemId === id);

  if (item) {
    return Object.fromEntries(Object.entries(item));
  }
};

// Create an Express application
const app = express();
// Create a Redis client
const client = createClient();
// Define the port number
const PORT = 1245;

// Function to reserve stock for a given item
const reserveStockById = async (itemId, stock) => {
  return promisify(client.SET).bind(client)(`item.${itemId}`, stock);
};

// Function to get the current reserved stock for a given item
const getCurrentReservedStockById = async (itemId) => {
  return promisify(client.GET).bind(client)(`item.${itemId}`);
};

// Route to get the list of products
app.get('/list_products', (_, res) => {
  res.json(listProducts);
});

// Route to get product details by item ID
app.get('/list_products/:itemId(\\d+)', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const productItem = getItemById(Number.parseInt(itemId));

  if (!productItem) {
    res.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((result) => Number.parseInt(result || 0))
    .then((reservedStock) => {
      productItem.currentQuantity = productItem.initialAvailableQuantity - reservedStock;
      res.json(productItem);
    });
});

// Route to reserve a product by item ID
app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const productItem = getItemById(Number.parseInt(itemId));

  if (!productItem) {
    res.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((result) => Number.parseInt(result || 0))
    .then((reservedStock) => {
      if (reservedStock >= productItem.initialAvailableQuantity) {
        res.json({ status: 'Not enough stock available', itemId });
        return;
      }
      reserveStockById(itemId, reservedStock + 1)
        .then(() => {
          res.json({ status: 'Reservation confirmed', itemId });
        });
    });
});

// Function to reset product stock in Redis
const resetProductsStock = () => {
  return Promise.all(
    listProducts.map(
      item => promisify(client.SET).bind(client)(`item.${item.itemId}`, 0),
    )
  );
};

// Start the server
app.listen(PORT, () => {
  resetProductsStock()
    .then(() => {
      console.log(`API available on localhost port ${PORT}`);
    });
});

// Export the Express app
export default app;
