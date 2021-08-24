from time import time

def time_func(func):
	def wrap_func(*args, **kwargs):
		t1 = time()
		result = func(*args, **kwargs)
		t2 = time()
		print(f'>>> function {func.__name__!r} executed in {(t2-t1):.6f}s')
		return result
	return wrap_func
