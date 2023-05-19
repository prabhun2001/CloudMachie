from motor.motor_asyncio import AsyncIOMotorClient

try:
    client = AsyncIOMotorClient("mongodb://23.21.228.145:27017")

    # Access database and collection
    database = client.clouddata
    collection1 = database.users
    collection2 = database.files 
       
except Exception as e:
        print("Error:", str(e))

