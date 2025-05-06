# Order Matching Engine

A simple implementation of an **Order Matching Engine** for financial markets. This project simulates the processing of **limit** and **market orders**, managing buy and sell orders in an order book, and executing trades when conditions are met.

The system supports the following features:
- **Limit Orders**: Orders placed at a specific price or better.
- **Market Orders**: Orders that are executed immediately at the best available price.
- **Order Book**: An internal system that stores buy and sell orders and ensures they are matched properly.
- **Order Cancellation**: Allows the cancellation of unexecuted limit orders.

## Features
- **Limit Order Book**: Supports both buy and sell orders, using a max-heap for buy orders and a min-heap for sell orders.
- **Market Order Matching**: Market orders are executed immediately against the best available orders.
- **Trade History**: Keeps track of executed trades with details of the quantity and price.
- **Order Cancellation**: You can cancel limit orders that have not been matched yet.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/order-matching-engine.git
   cd order-matching-engine
