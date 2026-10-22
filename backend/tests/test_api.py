import pytest
from fastapi.testclient import TestClient
import os
import sys

# Ensure backend root is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["developer"] == "Fardeen Akmal"

def test_get_stats():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_investigations" in data
    assert "supported_sources_count" in data

def test_username_investigation():
    response = client.post("/api/investigate/username", json={"username": "fardeenakmal"})
    assert response.status_code == 200
    data = response.json()
    assert data["target"] == "fardeenakmal"
    assert data["total_sources"] == 10
    assert "findings" in data
    assert len(data["findings"]) == 10
    assert "id" in data

def test_username_validation_error():
    response = client.post("/api/investigate/username", json={"username": "a"})
    # min_length=2 should trigger 422
    assert response.status_code == 422

def test_domain_investigation():
    response = client.post("/api/investigate/domain", json={"domain": "example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["target"] == "example.com"
    assert "dns_records" in data
    assert "registration" in data
    assert "id" in data

def test_domain_validation_error():
    response = client.post("/api/investigate/domain", json={"domain": "nodotdomain"})
    assert response.status_code == 400

def test_history_and_report_export():
    # 1. Check history
    h_resp = client.get("/api/history")
    assert h_resp.status_code == 200
    history = h_resp.json()
    assert len(history) > 0
    inv_id = history[0]["id"]
    
    # 2. Check single history record
    s_resp = client.get(f"/api/history/{inv_id}")
    assert s_resp.status_code == 200
    
    # 3. Check PDF report download
    pdf_resp = client.get(f"/api/reports/pdf/{inv_id}")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert len(pdf_resp.content) > 1000
    
    # 4. Check CSV report download
    csv_resp = client.get(f"/api/reports/csv/{inv_id}")
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers["content-type"]
    assert b"TRACE OSINT INVESTIGATION REPORT" in csv_resp.content

def test_history_deletion():
    # Create test record to delete
    create_resp = client.post("/api/investigate/username", json={"username": "tempdeltest"})
    assert create_resp.status_code == 200
    del_id = create_resp.json()["id"]
    
    # Delete it
    del_resp = client.delete(f"/api/history/{del_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["success"] is True
    
    # Verify 404 on subsequent get
    get_del = client.get(f"/api/history/{del_id}")
    assert get_del.status_code == 404
