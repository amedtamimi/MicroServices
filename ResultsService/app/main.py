from fastapi.responses import HTMLResponse ,RedirectResponse
from fastapi import FastAPI, Request, Form, HTTPException
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import os
from jinja2 import Environment, FileSystemLoader
import aiohttp


app = FastAPI()


mongo_client = MongoClient("mongodb://mongo:27017", username="root", password="example")
mongo_db = mongo_client["analytics_db"]
mongo_collection = mongo_db["statistics"]

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("html/index.html")

@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    auth_url = "http://host.docker.internal:49100/Auth.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(auth_url) as resp:
            auth = await resp.json()
    if form_data["Email"] == auth["Email"] and form_data["Password"] == auth["Password"]:
        response = RedirectResponse(url="/statistics")
        return response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

@app.post("/statistics")
async def get_statistics():
    statistics = list(mongo_collection.find({}))
    statistics_json = dumps(statistics)

    rendered_template = template.render(statistics=statistics)

    return HTMLResponse(content=rendered_template, status_code=200)


@app.get("/")
async def loginPage():
    with open("html/login.html", "r") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)
