# 1. Allow users to manage trading accounts
# 2. Allow users to buy and sell stocks
# 3. View portfolio of stocks



from enum import Enum
from collections import deque, defaultdict


# Constants
class OrderStatus(Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"

# Entities
class User:
    def __init__(
        self,
        _id: int,
        name: str,
    ):
        self.id = _id
        self.name = name

    def __str__(self):
        return f"{self.id=} {self.name=}"

class Account:
    def __init__(
        self,
        _id: int,
        user_id: int
    ):
        self.id = _id
        self.user_id = user_id
        self.balance = 0
        self.portfolio = Portfolio(self)

    def add_balance(self, amount: float):
        self.balance += amount
    
    def deduct_balance(self, amount: float):
        self.balance -= amount

    def get_balance(self) -> float:
        return self.balance
    
    def __str__(self):
        return f"{self.balance=}"


class Stock:
    def __init__(self, _id: int, symbol: str, name: str, price: str):
        self.id = _id
        self.symbol = symbol
        self.name = name
        self.price = price

    def update_price(self, price: float):
        self.price = price
    
    def __str__(self):
        return f"{self.symbol=} {self.name=} {self.price=}"

class Order:
    def __init__(self, _id: int, symbol: str, account_id: int, quantity: int, price: float):
        self.id = _id
        self.state = OrderStatus.PENDING
        self.stock_symbol = symbol
        self.account_id = account_id 
        self.quantity = quantity
        self.price = price

class BuyOrder(Order):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def execute(self):
        account = sb.get_account(self.account_id)
        balance = account.get_balance()

        total_cost = self.quantity * self.price
        if total_cost <= balance:
            account.deduct_balance(total_cost)
            account.portfolio.stocks[self.stock_symbol] += self.quantity
            self.state = OrderStatus.EXECUTED
        else:
            self.state = OrderStatus.REJECTED

class SellOrder(Order):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        account =  sb.get_account(self.account_id)

        available_quantity = account.portfolio.stocks[self.stock_symbol]
        
        total_proceeds = self.quantity * self.price

        if self.quantity <= available_quantity:
            account.add_balance(total_proceeds)
            account.portfolio.stocks[self.stock_symbol] -= self.quantity
            self.state = OrderStatus.EXECUTED
        else:
            self.state = OrderStatus.REJECTED


class Portfolio:
    def __init__(self, account: Account):
        self.stocks = defaultdict(int)
        self.account = account

    def __str__(self):
        return f"{self.stocks=}"

# Services
class StockBroker:
    def __init__(self):
        self.order_queue = deque([])
        self.accounts = {}
        self.users = {}
        self.stocks = {}
        self.orders = {}

    def create_user(
        self,
        _id: int,
        name: str
    ) -> User:
        usr = User(_id=_id, name=name)
        self.users[_id] = usr
        
        return usr
    
    def create_account(
        self,
        _id: int,
        user_id: int
    ) -> Account:

        ac = Account(_id=_id, user_id=user_id)
        self.accounts[_id] = ac
        return ac

    def get_account(self, account_id: int) -> Account:
        return self.accounts[account_id]

    def add_balance(self, account_id: int, amount: float):
        ac = self.get_account(account_id=account_id)
        ac.add_balance(amount=amount)

    def add_stock(self, symbol: str, name: str, price: str):
        stk = Stock(_id=symbol, symbol=symbol, name=name, price=price)

        self.stocks[symbol] = stk

        return stk
    
    def get_stock(self, symbol: str) -> Stock:
        return self.stocks[symbol]

    def stock_tick(self, symbol: str, price: float):
        stk = self.get_stock(symbol=symbol)
        stk.update_price(price)

        self.stocks[stk.id] = stk

    def create_order(
        self, 
        _id: int, 
        symbol: str, 
        account_id: int, 
        quantity: int, 
        price: float,
        buy: bool = True
    ) -> Order:

        ocls = BuyOrder if buy else SellOrder
        
        ordr = ocls(_id=_id, symbol=symbol, account_id=account_id, quantity=quantity, price=price)
        self.orders[_id] = ordr
        
        return ordr

    def place_order(self, order: Order):
        self.order_queue.appendleft(order)

    def process_orders(self):
        while self.order_queue:
            if not self.order_queue: continue

            next_order = self.order_queue.pop()
            
            next_order.execute()
    def __str__(self):
        return f"{self.orders=}"

# Test Cases

sb = StockBroker()

usr = sb.create_user(_id=1, name="Arpit")
ac = sb.create_account(_id=10, user_id=usr.id)

sb.add_balance(account_id=ac.id, amount=1000)

stk = sb.add_stock(symbol="ZOMATO", name="ZOMATO", price=100)

ordr = sb.create_order(_id=100, symbol="ZOMATO", account_id=ac.id, quantity=2, price=stk.price, buy=True)

sb.place_order(order=ordr)

ordr = sb.create_order(_id=101, symbol="ZOMATO", account_id=ac.id, quantity=1, price=stk.price, buy=False)

sb.place_order(order=ordr)

sb.process_orders()


for ac in sb.accounts.values():
    print(ac)
    print(ac.portfolio)









