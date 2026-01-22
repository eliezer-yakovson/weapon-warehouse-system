from fastapi import FastAPI, File, UploadFile
import pandas as pd
from db import create_connection, create_table, insert_data

app = FastAPI()

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        
        df['risk_level'] = pd.cut(df['range_km'], 
                                  bins=[-1, 20, 100, 300, float('inf')],
                                  labels=['low', 'medium', 'high', 'extreme'])
        
        df['manufacturer'].fillna('Unknown', inplace=True)

        conn = create_connection()
        create_table(conn)
        inserted_count = insert_data(conn, df)
        conn.close()

        return {"status": "success", "inserted_records": inserted_count}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)