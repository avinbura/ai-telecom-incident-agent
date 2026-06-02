# AI Telecom Network Incident Resolution Agent

This is a beginner-friendly Agentic AI project built using FastAPI and LangGraph.

## Project Overview

This project analyzes telecom network alerts and provides:

- Severity classification
- Tower log analysis
- Root cause identification
- Escalation decision
- SOP-based guidance
- Incident summary

## Tech Stack

- Python
- FastAPI
- LangGraph
- JSON
- Uvicorn

## Project Flow

User sends a telecom alert with tower ID, packet loss, and latency.

The system then follows this workflow:

1. Analyze alert severity
2. Retrieve tower logs
3. Read telecom SOP guidelines
4. Identify root cause
5. Recommend action
6. Decide escalation
7. Generate incident summary

## API Endpoint

```text
POST /analyze-alert
Version 3 added:
- ChromaDB vector database
- RAG-based SOP retrieval
- LLM Gateway with fallback handling
- Multi-agent execution tracking
- Postman API testing
- Incident history APIs


## Version 4 - Kafka Event Streaming

Version 4 adds real-time telecom event streaming using Kafka.

### New Features

- Kafka producer for simulated telecom alerts
- Kafka consumer for receiving streaming alerts
- Consumer automatically calls FastAPI `/analyze-alert`
- Events are processed by LangGraph multi-agent workflow
- Results are stored in PostgreSQL
- Redis prevents duplicate repeated processing

### Kafka Flow

```text
Kafka Producer
    ↓
telecom-alerts topic
    ↓
Kafka Consumer
    ↓
FastAPI /analyze-alert
    ↓
LangGraph Multi-Agent Workflow
    ↓
PostgreSQL Incident Storage


## Version 5 - PySpark, Databricks, and Delta Lake

Version 5 adds the data engineering layer to the Telecom AI Incident Agent project.

### New Data Sources

- Hugging Face telecom customer dataset
- Synthetic telecom incident dataset with 10,000 records
- PostgreSQL incident export from the application database

### New Features

- PySpark analytics pipeline
- Multi-source CSV ingestion
- Databricks notebook execution
- Delta Lake table creation
- Bronze/Silver/Gold data architecture

### Data Lake Architecture

```text
Raw CSV Data
    ↓
Bronze Table - raw telecom incidents
    ↓
Silver Table - cleaned and deduplicated incidents
    ↓
Gold Table - analytics-ready KPIs

