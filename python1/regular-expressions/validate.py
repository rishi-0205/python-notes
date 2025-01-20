import re

email = input("What's your email? ").strip()

if re.search(r"^(\w|.)+@(\w|.)+\.edu$", email, re.IGNORECASE):
    print("Valid")
else:
    print("Invalid")


# .       any char except a new line
# *       0 or more repetitions
# +       1 or more repetitions
# ?       0 or 1 repetitions
# {m}     m repetitions
# {m,n}   m-n repetitions
# \       Used as an escape character
# ^       Matches start of the string
# $       Matches end of the string
# []      Set of characters
# [^]     Complementing the set
# \w      Any word character(Alphanumberic and underscore)
# \D      Not a decimal digit
# \s      Whitespace Characters
# \S      Not a whitespace Character
# \W      Not a word character
# A|B     Either A or B
# (...)   A group
# (?:...) Non-capturing version