from fastapi import FastAPI, UploadFile, File
import pandas as pd


app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)