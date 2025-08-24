from stlr import Stlr
from stlr.Enum.HTTP import Method

site:Stlr = Stlr()

@site.route("/",[Method.GET])
def index():
	return "Hello!"

if __name__ == "__main__":
	# Running using the cli command
	# stlr run test_site.py
	# accomplishes the same behaviour.
	site.run("0.0.0.0",port=8081)
