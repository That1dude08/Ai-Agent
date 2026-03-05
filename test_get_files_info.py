from functions.get_files_info import get_files_info

print("Result for current directory:")
print(f"{get_files_info('calculator', '.')}")

print("Result for 'pkg' directory:")
print(f"{get_files_info('calculator', 'pkg')}")

print("Result for '/bin' directory:")
print(f"{get_files_info('calculator', '/bin')}")

print("Result for '../' directory:")
print(f"{get_files_info('calculator', '../')}")