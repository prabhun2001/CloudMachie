from database import collection2
from fastapi import FastAPI, Request
from bson import ObjectId 
from crypto_graphy.signature_decryption import decrypt_signature


# app object
app = FastAPI(debug=True)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/signup")
async def create_user(user: dict):

    try:
        user1 = {
            "_id": ObjectId(user["_id"]),
            "password": user["password"] ,
            "dob": user["dob"],
            "file_ids": []
        }

        result = await collection1.insert_one(user1)

        return {"message": "User created successfully", "user_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/login")
async def get_allfiles(user: dict):

    try:
        result = await collection1.find_one({"_id": ObjectId(user["_id"])})
        if result is not None and "file_ids" in result:
            files = {"all_files": []}
            for id in result["file_ids"]:
                file_result = await collection2.find_one({"_id": id})
                if file_result:
                    files["all_files"].append({"file_id": str(file_result["_id"]), "name": file_result["name"]})
                else:
                    return {"error": "file missing"}
            return files
        else:
            return {"message": "Document or field not found"}
    
    except Exception as e:
        return {"error": str(e)}


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
            return {"error": "failed decryptoin"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/getfile")
async def get_file(user: dict, file: dict):

    try:
        user_result = await collection1.find_one({"_id": ObjectId(user["_id"])})
        if user_result is not None:
            file_result = await collection2.find_one({"_id": ObjectId(file["_id"])})
            if file_result is not None:
                return {"name": file_result['name'], "data": file_result["data"]}
            else: 
                return {"error": "file not exist"}
        else:
            return {"error": "user not exist or file not exist"}
    except Exception as e:
        return {"error": str(e)}
