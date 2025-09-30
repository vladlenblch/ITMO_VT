import time

start = time.perf_counter()
for i in range(100):
    import inf_lab4
end = time.perf_counter()
print(f"Код: {end - start}")

start = time.perf_counter()
for i in range(100):
    import inf_lab4_1
end = time.perf_counter()
print(f"библиотеки: {end - start}")

start = time.perf_counter()
for i in range(100):
    import inf_lab4_2
end = time.perf_counter()
print(f"регулярки: {end - start}")

start = time.perf_counter()
for i in range(100):
    import inf_lab4_3
end = time.perf_counter()
print(f"формальные грамматики: {end - start}")
