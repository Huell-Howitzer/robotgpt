from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector

_print_ = PrintCollector
_getattr_ = getattr

src = \
'''
print("Hello World!")
result = printed
'''

code = compile_restricted(src, '<string>', 'exec')
exec(code)
print(result)