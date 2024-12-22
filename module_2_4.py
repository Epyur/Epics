number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
primes = []
not_primes =[]
is_primes = True
number.remove(1)
for i in number:
	for j in number:
		if i % j == 0 and i == j:
			primes.append(i)
		elif i % j == 0 and j < i:
			is_primes = False
			if is_primes:
				True
			else:
				not_primes.append(i)
			break
		
print("It's primes -", primes)
print("It's not primes -", not_primes)