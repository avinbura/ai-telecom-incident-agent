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