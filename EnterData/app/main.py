from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import aiohttp


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


# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='root',
                                host='mysql', database='db')

@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    auth_url = "http://host.docker.internal:49100/Auth.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(auth_url) as resp:
            auth = await resp.json()
    if form_data["Email"] == auth["Email"] and form_data["Password"] == auth["Password"]:
        response = RedirectResponse(url="/gradesPage")
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.post("/gradesApi")
async def create_grade(request: Request):
    # Save data to database
            form_data = await request.form()
            student_name = form_data["student_name"]
            course = form_data["course"]
            grade = form_data["grade"]
            date = form_data["date"]
            # Save data to database
            cursor = cnx.cursor()
            add_grade = ("INSERT INTO grades"
                            "(student_name, course, grade, date) "
                            "VALUES (%s, %s, %s, %s)")
            data_grade = (student_name, course, grade, date)
            cursor.execute(add_grade, data_grade)
            cnx.commit()
            cursor.close()
            return {"message": "Grade saved successfully."}
    


@app.post("/gradesPage")
async def gradesPage():
    with open("html/index.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)


@app.get("/")
async def loginPage():
    with open("html/login.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)
