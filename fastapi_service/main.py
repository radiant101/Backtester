from fastapi import FastAPI
from fastapi_service.routes.yfinance_routes import router
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()  #created an instance

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://127.0.0.1:8001"],        # <-- origins that are allowed
  allow_credentials=True,       # allow cookies, Authorization headers
  allow_methods=["*"],          # allow GET, POST, PUT, etc.
  allow_headers=["*"],          # allow all custom headers
)



@app.get('/')
def read_root():
     return {"mesaage":"hello fastapi"}
       
app.include_router(router)
