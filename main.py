import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from schemas import Creativelead
from database import create_document

app = FastAPI(title="Creative Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/api/ping")
def ping():
    return {"status": "ok"}

@app.post("/api/onboarding/lead")
def create_lead(lead: Creativelead):
    try:
        lead_id = create_document("creativelead", lead)
        return {"ok": True, "id": lead_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/services")
def services():
    return {
        "services": [
            {
                "id": "brand",
                "title": "Brand Identity",
                "description": "Strategy, naming, and visual systems that stand out.",
            },
            {
                "id": "product",
                "title": "Product Design",
                "description": "UX/UI for mobile and web with motion and micro-interactions.",
            },
            {
                "id": "web",
                "title": "Web Experiences",
                "description": "High-performance websites with 3D and immersive visuals.",
            },
            {
                "id": "content",
                "title": "Content & Campaigns",
                "description": "Launch creative with video, social, and performance assets.",
            },
        ]
    }

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
