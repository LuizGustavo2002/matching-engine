from matching_engine import Order, OrderBook

engine = OrderBook()

engine.add_order(Order(order_type="limit", side="buy", price=100, quantity=10))
engine.print_order_book()
engine.print_trade_history()

engine.add_order(Order(order_type="limit", side="sell", price=105, quantity=8))
engine.print_order_book()
engine.print_trade_history()

engine.add_order(Order(order_type="limit", side="sell", price=101, quantity=5))
engine.print_order_book()
engine.print_trade_history()

engine.cancel_order(2)
engine.print_order_book()
engine.print_trade_history()

engine.add_order(Order(order_type="limit", side="buy", price=102, quantity=6))
engine.print_order_book()
engine.print_trade_history()

engine.add_order(Order(order_type="market", side="sell", quantity=7))
engine.print_order_book()
engine.print_trade_history()
