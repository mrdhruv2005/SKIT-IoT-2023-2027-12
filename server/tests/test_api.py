"""Tests for the Chandas API endpoints."""

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("development")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_analyze_endpoint_success(client):
    """Test full analysis of a known verse (BG 1.1)."""
    response = client.post("/api/chandas/analyze", json={
        "text": "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः। मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय॥",
        "script": "devanagari"
    })
    
    assert response.status_code == 200
    data = response.json
    
    assert data["script_detected"] == "devanagari"
    assert len(data["padas"]) == 4
    
    meter = data["meter"]
    assert meter["identified"] is True
    assert meter["name"] == "Anuṣṭubh"
    assert meter["tier_used"] == 1


def test_analyze_endpoint_no_text(client):
    """Test analysis with missing text."""
    response = client.post("/api/chandas/analyze", json={})
    assert response.status_code == 400
    assert "error" in response.json


def test_syllabify_endpoint(client):
    """Test syllabification endpoint."""
    response = client.post("/api/chandas/syllabify", json={
        "text": "राम",
        "script": "devanagari"
    })
    
    assert response.status_code == 200
    data = response.json
    
    assert data["total_syllables"] == 2
    assert len(data["syllables"][0]) == 2
    assert data["syllables"][0][0]["text"] == "रा"
    assert data["syllables"][0][1]["text"] == "म"


def test_list_meters(client):
    """Test listing meters."""
    response = client.get("/api/chandas/meters?per_page=5")
    assert response.status_code == 200
    data = response.json
    
    assert "meters" in data
    assert len(data["meters"]) == 5
    assert data["total"] > 0


def test_get_meter(client):
    """Test getting a specific meter."""
    response = client.get("/api/chandas/meters/indravajra")
    assert response.status_code == 200
    data = response.json
    
    assert "meter" in data
    assert data["meter"]["id"] == "indravajra"
    assert data["meter"]["name_iast"] == "Indravajrā"


def test_get_meter_not_found(client):
    """Test getting a non-existent meter."""
    response = client.get("/api/chandas/meters/nonexistent")
    assert response.status_code == 404
