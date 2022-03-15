def float_range(min, max, step = 1):
	if max < min:
		min, max = max, min
	while min < max:
		yield min
		min += step