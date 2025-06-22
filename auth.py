import hashlib
import jwt
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up(username, email, password):
    user_exists = supabase.table("users").select("*").eq("email", email).execute()
    if user_exists.data:
        return "Email already registered!"
    
    hashed_pw = hash_password(password)
    supabase.table("users").insert({
        "username": username,
        "email": email,
        "password": hashed_pw
    }).execute()
    
    token = jwt.encode(
            {
            "email": email, 
            "username": username
            },
            JWT_SECRET, 
            algorithm = "HS256"
        )
    
    return {"message": "Account Created Successfully", "token": token}

def sign_in(email, password):
    response = supabase.table("users").select("*").eq("email", email).execute()
    users = response.data

    if not users:
        return "Invalid Email !"
    
    user = users[0]
    hashed_input_pw = hash_password(password)

    if hashed_input_pw != user["password"]:
        return "Wrong password. Try again."
    
    token = jwt.encode(
        {
            "email": user["email"],
            "username": user["username"]
        },
        JWT_SECRET,
        algorithm = "HS256"
    )

    return {"message": "Signed in successfully", "token": token}

# def verify_token(token):
#     try:
#         decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#         return {"valid": True, "data": decoded}
#     except jwt.ExpiredSignatureError:
#         return {"message": "Expired Token", "valid": False}
#     except jwt.InvalidTokenError:
#         return {"message": "Invalid Token", "valid": False}

def decode_token(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"message": "Expired Token"}
    except jwt.InvalidTokenError:
        return {"message": "Invalid Token"}

# def insert_currency_data(token, pair, price, time, date):
#     auth_result = verify_token(token)

#     if not auth_result["valid"]:
#         return {"message": "Token Invalid or Expired"}
    
#     user_email = auth_result["data"]["email"]

#     supabase.table("currency_data").insert({
#         "email": user_email,
#         "pair": pair,
#         "price": price,
#         "time": time,
#         "date": date
#     }).execute()

#     return "Data saved successfully !"

# if __name__ == "__main__":
#     result = sign_in("chanh@gmail.com", "123456789")
#     token = result.get("token")
#     if token:
#         verify_result = verify_token(token)
#         print("Result: ", verify_result)
#     else:
#         print("Login Failed")
#     print(result)