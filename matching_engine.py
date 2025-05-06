import heapq
import itertools


class Order:
    _ids = itertools.count(1)

    def __init__(self, order_type, side, quantity, price=None):
        self.id = next(Order._ids)
        self.type = order_type  # 'limit' or 'market'
        self.side = side        # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity
        self.active = True  # Used for cancellation

    def __repr__(self):
        return (f"Order(id={self.id}, type={self.type}, side={self.side}, "
                f"price={self.price}, quantity={self.quantity}, active={self.active})")


class OrderBook:
    def __init__(self):
        self.buy_orders = []   # Max-heap for buy orders
        self.sell_orders = []  # Min-heap for sell orders
        self.order_map = {}    # id -> order
        self.trade_history = []

    def add_order(self, order):
        self.order_map[order.id] = order

        if order.type == "market":
            self._execute_market_order(order)
        elif order.type == "limit":
            self._execute_limit_order(order)
        else:
            print(f"Unknown order type: {order.type}")

    def cancel_order(self, order_id):
        order = self.order_map.get(order_id)
        if order and order.active and order.type == "limit":
            order.active = False
            print(f"Order {order_id} canceled.")
        else:
            print(f"Order {order_id} not found or cannot be canceled.")

    def _execute_market_order(self, order):
        if order.side == "buy":
            self._match_order(order, self.sell_orders, reverse=False)
        else:
            self._match_order(order, self.buy_orders, reverse=True)

    def _execute_limit_order(self, order):
        if order.side == "buy":
            self._match_order(order, self.sell_orders, reverse=False)
            if order.quantity > 0 and order.active:
                heapq.heappush(self.buy_orders, (-order.price, order.id, order))
        else:
            self._match_order(order, self.buy_orders, reverse=True)
            if order.quantity > 0 and order.active:
                heapq.heappush(self.sell_orders, (order.price, order.id, order))

        if order.quantity > 0 and order.active:
            print(f"Order {order.id} placed in the order book without an immediate match.")
        else:
            print(f"Order {order.id} was ignored because no immediate match was found.")

    def _match_order(self, incoming_order, book, reverse=False):
        while incoming_order.quantity > 0 and book:
            price, _, resting_order = book[0]

            if not resting_order.active:
                heapq.heappop(book)
                continue

            if reverse:
                price = -price  # Adjust actual price for max-heap

            if incoming_order.type == "limit":
                if incoming_order.side == "buy" and price > incoming_order.price:
                    break
                elif incoming_order.side == "sell" and price < incoming_order.price:
                    break

            trade_qty = min(incoming_order.quantity, resting_order.quantity)
            incoming_order.quantity -= trade_qty
            resting_order.quantity -= trade_qty

            self.trade_history.append({
                "price": price,
                "quantity": trade_qty,
                "buy_order_id": incoming_order.id if incoming_order.side == "buy" else resting_order.id,
                "sell_order_id": incoming_order.id if incoming_order.side == "sell" else resting_order.id
            })

            print(f"Trade Executed: {trade_qty} @ {price} (Buy ID: {incoming_order.id if incoming_order.side == 'buy' else resting_order.id}, "
                  f"Sell ID: {incoming_order.id if incoming_order.side == 'sell' else resting_order.id})")

            if resting_order.quantity == 0:
                resting_order.active = False
                heapq.heappop(book)

    def print_order_book(self):
        print("\nOrder Book:")
        print("Sell Orders:")
        for price, _, order in sorted(self.sell_orders):
            if order.active and order.quantity > 0:
                print(f"  {order.quantity} @ {price} (ID: {order.id})")
        print("Buy Orders:")
        for price, _, order in sorted(self.buy_orders, reverse=True):
            if order.active and order.quantity > 0:
                print(f"  {order.quantity} @ {-price} (ID: {order.id})")
        print("-" * 30)

    def print_trade_history(self):
        print("\nTrade History:")
        for trade in self.trade_history:
            print(f"  {trade['quantity']} @ {trade['price']} (Buy ID: {trade['buy_order_id']} | Sell ID: {trade['sell_order_id']})")
        print("-" * 30)
