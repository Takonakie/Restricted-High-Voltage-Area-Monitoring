# 🏭 Industrial Safety Monitoring Pipeline (High-Voltage Protection)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## 📖 Project Overview

**StairSafe / HV-Monitor** is an end-to-end Computer Vision pipeline designed to automate safety compliance in high-risk industrial environments. 

This prototype specifically addresses the challenge of **"High Voltage Panel Protection"** in manufacturing plants. Unlike passive CCTV recording, this system actively monitors exclusion zones in real-time, detects unauthorized access by personnel, and automatically triggers an ETL process to log incidents and capture visual evidence for HSE (Health, Safety, & Environment) audits.

### 🎯 The Problem
In busy factories, workers often overlook floor markings near critical electrical panels or robotic arms. Accidents in these zones can be fatal. Manual monitoring by safety officers via CCTV is inefficient and prone to human error.

### 💡 The Solution
An automated "Virtual Fence" system that:
1.  **Detects** human presence using YOLOv8.
2.  **Validates** spatial intrusion using polygon overlap logic.
3.  **Logs** critical violations into a structured SQL database.
4.  **Captures** snapshot evidence automatically.
5.  **Visualizes** safety KPIs via a real-time dashboard.

---

## 📸 Demo Previews

### 1. Real-time Intrusion Detection
*The system detects a worker entering the High Voltage exclusion zone.*
![Detection Demo](demo_image/demo_detection.jpg) 

### 2. HSE Monitoring Dashboard
*Managers can view live statistics and photographic evidence of violations.*
![Dashboard Demo](demo_image/demo_dashboard.png)

---

## 🏗️ System Architecture

### 1. Current Prototype (Edge Logic)
The data flow currently running on the local machine:

```mermaid
graph LR
    A[Camera Feed] -->|Frame Stream| B(YOLOv8 Inference)
    B -->|Bbox Coordinates| C{Spatial Logic}
    C -->|Safe| D[Discard Frame]
    C -->|Zone Intrusion!| E[Trigger Incident]
    E -->|1. Save Snapshot| F[Local Storage /evidence]
    E -->|2. Insert Metadata| G[(SQLite Database)]
    G -->|Query| H[Streamlit Dashboard]