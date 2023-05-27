from database import collection2
from fastapi import FastAPI, Request
from bson import ObjectId 
from crypto_graphy.signature_decryption import decrypt_signature


# app object
app = FastAPI(debug=True)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# @app.post("/signup")
# async def create_user(user: dict):

#     try:
#         user1 = {
#             "_id": ObjectId(user["_id"]),
#             "password": user["password"] ,
#             "dob": user["dob"],
#             "file_ids": []
#         }

#         result = await collection1.insert_one(user1)

#         return {"message": "User created successfully", "user_id": str(result.inserted_id)}
#     except Exception as e:
#         return {"error": str(e)}

# @app.post("/login")
# async def get_allfiles(user: dict):

#     try:
#         result = await collection1.find_one({"_id": ObjectId(user["_id"])})
#         if result is not None and "file_ids" in result:
#             files = {"all_files": []}
#             for id in result["file_ids"]:
#                 file_result = await collection2.find_one({"_id": id})
#                 if file_result:
#                     files["all_files"].append({"file_id": str(file_result["_id"]), "name": file_result["name"]})
#                 else:
#                     return {"error": "file missing"}
#             return files
#         else:
#             return {"message": "Document or field not found"}
    
#     except Exception as e:
#         return {"error": str(e)}


@app.post("/upload")
async def upload_file(request: Request):
    try:
        data = await request.json()
        signature = request.headers.get("Signature")
        print(decrypt_signature(signature))
        if decrypt_signature(signature):
            file_result = await collection2.insert_one({"filename": data["filename"],"content": data["content"],"authorized_users": data["authorized_users"]})
            return {"file_id": str(file_result.inserted_id)}
        else:
            return {"error": "failed decryptoin"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/getfiles")
async def get_all_files(request: Request):
    try:
        signature = request.headers.get("Signature")
        decrypted_signature = decrypt_signature(signature)
        user_id = decrypted_signature.split("+")[0]
        print(user_id)

        if decrypted_signature:
            files = await collection2.find().to_list(length=None)
            serialized_files = []
            for file in files:
                authorized_users = file["authorized_users"]
                if user_id in authorized_users:
                    serialized_file = {
                        "filename": file["filename"],
                        "file_id": str(file["_id"])
                    }
                    serialized_files.append(serialized_file)

            return {"files": serialized_files}
        else:
            return {"error": "signature not valid"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/getfile")
async def get_file(request: Request):
    try:
        signature = request.headers.get("Signature")
        decrypted_signature = decrypt_signature(signature)
        file_id = decrypted_signature.split("+")[2]
        print(file_id)

        if decrypted_signature:
            result = await collection2.find_one({"_id": ObjectId(file_id)})
            if result is not None:
                return {"filename": result["filename"],"content": result["content"]}
            else:
                return {"error": "file not exist in storage!!!"}
        else:
            return {"error": "signature not valid"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/delete")
async def delete_file(request: Request):
    try:
        signature = request.headers.get("Signature")
        decrypted_signature = decrypt_signature(signature)
        file_id = decrypted_signature.split("+")[2]
        user_id = decrypted_signature.split("+")[0]
        print(file_id)
        print(user_id)

        if decrypted_signature:
            result = await collection2.find_one({"_id": ObjectId(file_id)})
            if result is not None:
                # Get the authorized users list
                authorized_users = result.get("authorized_users", [])
                # Check if the user's ID is in the authorized users list
                if user_id in authorized_users:
                    # Remove the user from the authorized users list
                    authorized_users.remove(user_id)

                    # If the authorized users list becomes empty, delete the file
                    if len(authorized_users) == 0:
                        await collection2.delete_one({"_id": ObjectId(file_id)})
                    else:
                        # Update the authorized users list in the database
                        await collection2.update_one(
                            {"_id": ObjectId(file_id)},
                            {"$set": {"authorized_users": authorized_users}}
                        )
                    return {"status": "deleted"}

                else:
                    return {"error": "user not found"}
            else:
                return {"error": "file not exist in storage!!!"}
        else:
            return {"error": "signature not valid"}
    except Exception as e:
        return {"error": str(e)}

