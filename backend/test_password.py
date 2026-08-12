from app.auth.password import hash_password, verify_password 

password = "Admin@123"

hashed_password = hash_password(password)

print("Original:", password)
print("Hash:", hashed_password)

print(
    "Correct:",
    "Verify:", verify_password(password, hashed_password)
)

print(
    "Wrong:" ,
    verify_password("WrongPassword", hashed_password)
)

