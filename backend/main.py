import os
import sys
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Ensure backend root is in sys.path
sys.path.append(os.path.dirname(__file__))

from database import (
    init_db, save_investigation, get_all_investigations,
    get_investigation_by_id, delete_investigation, clear_all_investigations, get_stats
)
from services.username_osint import investigate_username
from services.domain_osint import investigate_domain
from services.reporting import generate_pdf_report, generate_csv_report

init_db()

app = FastAPI(
    title="TRACE — OSINT Digital Footprint Analyzer",
    description="Cybersecurity Mini Project by Fardeen Akmal (Roll No: 2), Guide: Akanksha Thakare",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UsernameRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)

class DomainRequest(BaseModel):
    domain: str = Field(..., min_length=3, max_length=100)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "TRACE OSINT Analyzer",
        "version": "1.0.0",
        "developer": "Fardeen Akmal"
    }

@app.get("/api/stats")
def get_dashboard_stats():
    return get_stats()

@app.post("/api/investigate/username")
async def api_investigate_username(req: UsernameRequest):
    username = req.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
        
    result = await investigate_username(username)
    
    summary = f"Checked {result['total_sources']} sources: {result['found_count']} Found, {result['inconclusive_count']} Inconclusive, {result['not_found_count']} Not Found"
    status = "Completed" if result["found_count"] > 0 else ("Partial" if result["inconclusive_count"] > 0 else "Completed")
    
    inv_id = save_investigation("username", username, status, summary, result)
    result["id"] = inv_id
    result["summary"] = summary
    result["status"] = status
    return result

@app.post("/api/investigate/domain")
async def api_investigate_domain(req: DomainRequest):
    domain = req.domain.strip()
    if not domain or "." not in domain:
        raise HTTPException(status_code=400, detail="Please enter a valid domain name (e.g. example.com)")
        
    result = await investigate_domain(domain)
    
    ip = result.get("primary_ip", "Unknown")
    reg = result.get("registration", {}).get("registrar", "Unknown")
    summary = f"Resolved IP: {ip} | Registrar: {reg} | NS: {len(result['dns_records']['NS'])} records"
    status = "Completed" if ip != "Unknown" else "Partial"
    
    inv_id = save_investigation("domain", domain, status, summary, result)
    result["id"] = inv_id
    result["summary"] = summary
    result["status"] = status
    return result

@app.get("/api/history")
def get_history(limit: int = Query(50, ge=1, le=100)):
    return get_all_investigations(limit)

@app.get("/api/history/{inv_id}")
def get_single_history(inv_id: int):
    record = get_investigation_by_id(inv_id)
    if not record:
        raise HTTPException(status_code=404, detail="Investigation record not found")
    return record

@app.delete("/api/history/{inv_id}")
def delete_single_history(inv_id: int):
    success = delete_investigation(inv_id)
    if not success:
        raise HTTPException(status_code=404, detail="Investigation record not found")
    return {"success": True, "message": f"Investigation #{inv_id} deleted"}

@app.delete("/api/history")
def clear_history():
    clear_all_investigations()
    return {"success": True, "message": "All investigation records cleared"}

@app.get("/api/reports/pdf/{inv_id}")
def download_pdf_report(inv_id: int):
    record = get_investigation_by_id(inv_id)
    if not record:
        raise HTTPException(status_code=404, detail="Investigation record not found")
    filepath = generate_pdf_report(record)
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=os.path.basename(filepath)
    )

@app.get("/api/reports/csv/{inv_id}")
def download_csv_report(inv_id: int):
    record = get_investigation_by_id(inv_id)
    if not record:
        raise HTTPException(status_code=404, detail="Investigation record not found")
    filepath = generate_csv_report(record)
    return FileResponse(
        filepath,
        media_type="text/csv",
        filename=os.path.basename(filepath)
    )

# Mount static frontend build if it exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
