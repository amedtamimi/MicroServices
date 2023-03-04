from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient


app = FastAPI()


origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers    
)


mongo_client = MongoClient("mongodb://mongo:27017",username= 'root', password= 'example')
mongo_db = mongo_client["analytics_db"]
mongo_collection = mongo_db["statistics"]


@app.get("/")
async def generate_statistics():
    # Connect to MySQL database
    cnx = mysql.connector.connect(user='root', password='root',
                                host='mysql', database='db')
    cursor = cnx.cursor()
    cursor.execute(f"SELECT grade FROM grades")
    new_grades = [row[0] for row in cursor.fetchall()]
    print(new_grades)

    max_grade = max(new_grades)
    min_grade = min(new_grades)
    avg_grade = sum(new_grades) / len(new_grades)
    print(max_grade, min_grade, avg_grade)
    statistics = {
        "max_grade": max_grade,
        "min_grade": min_grade,
        "avg_grade": avg_grade
    }

    # Insert statistics to Mongo DB
    mongo_collection.insert_one(statistics)
    return {"message": "Statistics saved successfully."}
