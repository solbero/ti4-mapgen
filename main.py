from ti4_mapgen.views import app

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8005, log_level="info", reload=True)
