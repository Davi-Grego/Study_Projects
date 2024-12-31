from .earnings_services import EarningsServices
from .user_services import UserServices
from .expense_services import ExpenseServices
from .utils import Utils

def inject_services():
    return {"ExpenseServices": ExpenseServices,
                "UserServices": UserServices,
                "EarningsServices": EarningsServices,
                "Utils": Utils}
