# Requirements


# 1. Add Expense
# 2. Edit Expense
# 3. Settle Expense
# 4. Add group Expense
# 5. Simplify Expense
# 6. Comments and Activity Log

from heapq import heappush, heappop

# Entities
class User:
    def __init__(self, _id: int, name: str):
        self._id = _id
        self.name = name

class Group:
    def __init__(self, _id: int, name: str):
        self._id = _id
        self.name = name
        self.members: list[User] = []


class Amount:
    def __init__(self, amount: float, currency: str = '₹'):
        self.amount = amount
        self.currency = currency


class Expense:
    def __init__(
        self,
        _id: int,
        group_id: int,
        user_amount: dict
    ):
        self._id = _id
        self.group_id = group_id
        self.user_amount: dict[int, Amount] = user_amount


# Services

class ExpenseService:
    def __init__(self):
        self.expenses: dict[int, Expense] = {}

    def add_expense(
        self,
        _id: int,
        group_id: int,
        user_amount: dict[int, Amount]
    ) -> Expense:
        exp = Expense(_id=_id, group_id=group_id, user_amount=user_amount) 
        # validate that all users belong to the group
        self.expenses[_id] = exp
        return exp
    
    def simplify_group_expenes(self, group_id: int):
        expenses = [v for k, v in self.expenses.items() if v.group_id == group_id]
        
        total_user_amount: dict[int, float] = {}
        
        for expense in expenses:

            for user_id, amount in expense.user_amount.items():
                total_user_amount[user_id] = total_user_amount.get(user_id, 0) + amount

        print(f"{total_user_amount=}")
        receive, send = [], []

        for user_id, amount in total_user_amount.items():
            if amount < 0:
                heappush(send, (amount, user_id))
            elif amount > 0:
                heappush(receive, (-amount, user_id))
        
        res = []

        while receive and send:
            print(f"{receive=} {send=}")
            receive_top, send_top = heappop(receive), heappop(send)
            
            ra, ru = abs(receive_top[0]), receive_top[1]
            sa, su = abs(send_top[0]), send_top[1]

            diff = ra - sa

            res.append((su, ru, min(ra, sa)))
            
            if diff > 0:
                heappush(receive, (-diff, ru))
            elif diff < 0:
                heappush(send, (diff, su))
            
        return res            


class UserService:
    def __init__(self):
        self.users: dict[int, User] = {}

    def add_user(self, _id: int, name: str) -> User:
        usr = User(_id=_id, name=name)
        self.users[_id] = usr

        return usr

class GroupService:
    def __init__(self):
        self.groups: dict[int, Group] = {}

    def add_group(self, _id: int, name: str) -> Group:
        grp = Group(_id=_id, name=name)
        self.groups[_id] = grp

        return grp
    
    def add_member(self, group_id: int, user: User):
        self.groups[group_id].members.append(user)




us = UserService()

u1 = us.add_user(1, "A")
u2 = us.add_user(2, "B")
u3 = us.add_user(3, "C")

gs = GroupService()

gs.add_group(100, "NYC")
gs.add_member(100, u1)
gs.add_member(100, u2)
gs.add_member(100, u3)


es = ExpenseService()
es.add_expense(1000, 100, { 1: 20, 2: -30, 3: 10 })

print(es.simplify_group_expenes(100))




        
