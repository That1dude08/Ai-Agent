from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(len(result))  
print(result[-100:]) 

result = get_file_content("calculator", "main.py")
print(len(result))  
print(result) 

result = get_file_content("calculator", "pkg/calculator.py")
print(len(result))  
print(result) 

result = get_file_content("calculator", "/bin/cat")
print(len(result))  
print(result) 

result = get_file_content("calculator", "pkg/does_not_exist.py")
print(len(result))  
print(result) 
