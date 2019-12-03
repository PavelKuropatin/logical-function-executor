import re

DC = None
SUPPORTED_OPERATORS = ["||", "&", "~"]
U_OPERATORS = ["~"]
BI_OPERATORS = ["||", "&"]
RE_BRACKETS = re.compile("[()]")
