from stlr import Stlr
from stlr.Enum.HTTP import Method

site:Stlr = Stlr(__file__)

@site.route("/",[Method.GET])
def index():
    return "Hello!"

site.run("0.0.0.0",port=8081)
