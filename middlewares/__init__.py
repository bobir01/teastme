from loader import dp
from .throttling import ThrottlingMiddleware
from .check_sub import BigBrother


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(BigBrother())