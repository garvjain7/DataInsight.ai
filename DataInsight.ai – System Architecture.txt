# DataInsight.ai – System Architecture (Version 1.0)

**Document Version:** 1.0  
**Purpose:** Define the complete end-to-end system architecture for DataInsight.ai (Initial Design)  
**Scope:** Low-user phase (no distributed workers yet)  
**Authoring Context:** Backend + System Design perspective  

---

# 1. High-Level Architecture

DataInsight.ai is a multi-stage intelligent data analysis and reporting system that:

1. Accepts dataset uploads
2. Performs ETL and analytics
3. Detects ML problem type
4. Trains and evaluates a model
5. Generates a structured report
6. Creates a RAG-based conversational interface over the report

The system is designed around a **job-centric architecture**, where every dataset upload generates a unique `job_id` that tracks all stages of processing.

## Core Components

- **Frontend**: React application
- **API Layer**: Node.js (Express)
- **ML Engine**: Python service
- **Storage Layer**: In-memory (current), S3-compatible (future)
- **Vector Index**: Used for report-based retrieval
- **Job State Manager**: Maintains lifecycle of each dataset processing request

---

# 2. Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | React |
| API Layer | Node.js + Express |
| ML Engine | Python |
| File Upload | Multer |
| Storage (Current) | In-memory / local disk |
| Storage (Future) | S3-compatible object storage |
| Vector Index | FAISS / Pinecone / Qdrant (future decision) |
| Queue (Future) | Redis-based queue |

The system is designed so that changing storage or adding workers does **not require API changes**.

---

# 3. End-to-End Data Flow

## 3.1 Upload Phase

1. User uploads dataset
2. Backend generates unique `job_id`
3. Dataset is stored via storage abstraction layer
4. Job status initialized
5. Response returns `job_id`

Example UUID generation:

```js
import { v4 as uuidv4 } from 'uuid';

const jobId = uuidv4();
```

Example Upload Response:

```json
{
  "job_id": "c4f8b2b0-8a4e-4c4f-a8b5-73a9d3e0a912",
  "status": "uploaded"
}
```

---

## 3.2 Processing Stages

Each job progresses through defined states.

### Defined Job States

```
uploaded
etl_processing
etl_completed
ml_processing
ml_completed
report_generated
rag_indexed
completed
failed
```

This ensures deterministic lifecycle management.

---

# 4. Backend Architecture

The backend follows layered separation of concerns.

## 4.1 API Layer Responsibilities

- Accept file uploads
- Generate job_id
- Manage job state
- Expose status endpoints
- Serve metadata and analytics
- Provide chat endpoint

The API layer does **not**:

- Train models
- Perform heavy ETL
- Generate embeddings

It orchestrates the process.

---

## 4.2 Recommended API Structure

### Upload
```
POST /dataset/upload
```

### Job Status
```
GET /job/:id
```

### Metadata
```
GET /job/:id/metadata
```

### Analytics
```
GET /job/:id/analytics
```

### Report
```
GET /job/:id/report
```

### Chat
```
POST /chat/:job_id
```

This modular structure prevents coupling between stages.

---

# 5. Worker / ML Engine Architecture (Current + Future)

## Current (Low User Phase)

Processing may happen synchronously in a controlled flow.

## Future Phase

Processing will be delegated to worker processes via Redis queue.

Pipeline Stages:

1. Dataset Validation
2. ETL
3. Feature Engineering
4. Problem Type Detection
5. Model Training
6. Evaluation
7. Report Generation
8. Embedding Creation

Each stage must be logically independent.

---

# 6. Metadata Strategy

Metadata is the foundation of LLM grounding.

The raw dataset is **never sent to the LLM**.

Instead, structured metadata is extracted.

Example Metadata Structure:

```json
{
  "job_id": "...",
  "rows": 12000,
  "columns": 18,
  "column_types": {
    "age": "numerical",
    "gender": "categorical"
  },
  "missing_values": {
    "age": 2.3,
    "salary": 5.1
  },
  "class_distribution": {
    "0": 70,
    "1": 30
  },
  "problem_type": "classification",
  "target_source": "user | auto_detected"
}
```

Metadata ensures:

- Reduced hallucination
- Better LLM grounding
- Explainability
- Structured prompt construction

---

# 7. RAG Design Strategy

The RAG system operates only over structured report data.

## 7.1 Report Structure

The report is divided into semantic sections:

- Data Summary
- Model Summary
- Performance Metrics
- Feature Importance
- Limitations

## 7.2 Embedding Strategy

Do NOT embed raw JSON.

Instead:

- Convert report sections to readable structured text
- Chunk intelligently
- Generate embeddings per section

## 7.3 Prompt Construction

System prompt includes:

- Dataset metadata
- Problem type
- Model metrics

Retrieved context includes:

- Relevant report chunks

Example Prompt Structure:

```
System Context:
Dataset Summary: ...
Model Type: ...
Accuracy: ...

Relevant Sections:
...

User Question:
...
```

---

# 8. Storage Strategy

## Current Phase

- Dataset stored in memory or local disk

## Abstraction Layer

```
storageService.saveDataset()
storageService.getDataset()
```

Implementation now: in-memory map  
Implementation later: S3

This ensures API stability.

## Future Storage

| Data Type | Storage |
|------------|----------|
| Dataset | S3 |
| Metadata | Database |
| Report | Object Storage |
| Vector Index | Vector DB |

---

# 9. Failure Handling Strategy

Each stage must handle failure explicitly.

If failure occurs:

```
job.status = "failed"
job.error_message = "..."
```

Never leave job in ambiguous state.

Frontend must check job state before rendering analytics or chat.

---

# 10 Background Worker Architecture

## 10.1 Purpose of Workers

In production environments, heavy computational stages such as **ETL, analytics, model training, report generation, and vector indexing** must not execute within the API request lifecycle.

Workers are introduced to:

- ✅ Prevent API blocking
- ✅ Improve system scalability
- ✅ Enable horizontal scaling
- ✅ Isolate failures
- ✅ Provide retry and resilience mechanisms

> **Key Principle:** The logical stages of the system remain unchanged. Workers only change the execution mechanism.

---

## 10.2 High-Level Worker Flow

When worker mode is enabled:

```
1. User uploads dataset
2. Backend generates a unique job_id
3. Backend stores initial job state (UPLOADED)
4. Backend pushes job to Redis queue
5. Worker pulls job from queue
6. Worker executes pipeline stages sequentially
7. Worker updates job state after each stage
8. Results are stored and made available via API
9. Frontend polls or subscribes for status updates
```

---

## 10.3 Job Object Structure

Each processing request is represented as a **Job object**.

### Example Structure:

```json
{
  "job_id": "uuid-v4",
  "user_id": "optional",
  "dataset_path": "s3://bucket/dataset.csv",
  "status": "ETL_RUNNING",
  "target_column": "optional",
  "problem_type": null,
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "metadata": {},
  "report_path": null,
  "vector_index_path": null
}
```

### Job States:

| State | Description |
|-------|-------------|
| `UPLOADED` | File uploaded, waiting to process |
| `ETL_RUNNING` | Data extraction/transformation running |
| `ETL_COMPLETED` | ETL finished |
| `ANALYTICS_COMPLETED` | Analytics done |
| `TRAINING_RUNNING` | Model training in progress |
| `TRAINING_COMPLETED` | Training finished |
| `REPORT_GENERATED` | Report created |
| `INDEXED` | Vector index built |
| `COMPLETED` | All stages done |
| `FAILED` | Error occurred |

---

## 10.4 Queue Design (Redis)

Redis is used as a **job queue** for asynchronous processing.

### API Pushes Jobs:

```javascript
await redis.lpush("dataset_jobs", JSON.stringify(jobPayload));
```

### Workers Listen Continuously:

```javascript
while (true) {
    const job = await redis.brpop("dataset_jobs", 0);
    processJob(job);
}
```

### Blocking Pop (BRPOP) Benefits:

- ✅ No busy waiting
- ✅ Efficient CPU usage
- ✅ Real-time processing

---

## 10.5 Worker Execution Model

Each worker performs these steps:

1. Fetches job from queue
2. Validates dataset existence
3. Runs ETL stage
4. Generates metadata
5. Stores intermediate results
6. Runs model training
7. Generates report
8. Builds vector index
9. Marks job as COMPLETED

### Critical Design Rule:

> **Each stage must be idempotent and restart-safe**

If a worker crashes during training, the job can be retried without corrupting state.

---

## 10.6 Stage Isolation Principle

Each logical stage must be implemented as an **independent function**:

```python
def run_etl(job_id):
    # ETL logic
    pass

def run_training(job_id):
    # Training logic
    pass

def generate_report(job_id):
    # Report generation
    pass
```

The worker **orchestrates execution** but does not embed stage logic.

### Benefits:

- ✅ Reusability
- ✅ Testability
- ✅ Executor independence
- ✅ Easier migration to distributed systems

---

## 10.7 Status Tracking Strategy

Job state must be stored in:

- **Redis** — Fast access and real-time updates
- **Database** — Persistence (optional in early phase)

### Frontend Status Check:

```
GET /api/job/:job_id/status
```

### Example Response:

```json
{
  "job_id": "uuid",
  "status": "TRAINING_RUNNING",
  "progress": 65,
  "metadata_available": true,
  "report_available": false
}
```

---

## 10.8 Failure Handling Strategy

If any stage fails:

1. Worker catches exception
2. Job marked as `FAILED`
3. Error message stored in job metadata
4. Frontend notified
5. Optional retry policy applied

### Retry Strategies:

- **Immediate Retry** — Max 3 attempts (for transient errors)
- **Dead-Letter Queue** — Manual inspection (for persistent errors)

---

## 10.9 Horizontal Scaling  

Multiple workers can run **simultaneously** and consume from the same queue:

```
Worker-1 ─┐
Worker-2 ─┤
Worker-3 ─├──> Redis Queue ──> Process Jobs
Worker-4 ─┤
Worker-5 ─┘
```

### Redis Guarantees:

- ✅ Each job is processed by **only one worker**
- ✅ Load distribution happens **naturally**
- ✅ No job duplication

---

## 10.10 Transition Strategy (Current vs Future)

### Current Phase:
```
Synchronous execution (low user volume)
API handles all processing in request lifecycle
```

### Future Phase:
```
API only enqueues jobs
Workers execute heavy stages asynchronously
No change required in stage logic
```

> **Benefit:** This design ensures **forward compatibility** without rewriting the pipeline.

# 11. Scalability & Future Evolution Plan

## 11.1 Queue Introduction

Introduce Redis-based queue.

Flow:

```
Upload → Push Job → Worker Consumes → Process → Update State
```

## 11.2 Stage Isolation

Each stage can later be scaled independently.

## 11.3 Stateless API Layer

Node API must remain stateless.

## 11.4 Horizontal Scaling

Multiple workers can process independent job_ids.

---

# 12. Optional User Input Handling

Users may optionally provide:

- Target column
- Problem type

Logic:

```
if user_provided_target:
    validate and use
else:
    auto-detect
```

Transparency is stored in metadata.

---

# 13. Analytics Mid-Stage Strategy

When ETL completes:

1. Metadata saved
2. Analytics artifacts saved
3. Job state updated to `etl_completed`
4. Frontend polls status
5. Frontend fetches analytics

ML continues independently.

No blocking of pipeline.

---

# 14. Core Design Principles

- Job-centric architecture
- State-machine driven lifecycle
- Separation of orchestration and compute
- Metadata-first LLM grounding
- Storage abstraction
- Modular API endpoints
- Stage independence

---

# 15. Versioning Note

This is Version 1.0 of the system architecture.

Future versions may introduce:

- Distributed workers
- Microservice separation
- Event-driven architecture
- Multi-model orchestration
- Advanced monitoring and logging

This document establishes the foundational architecture for DataInsight.ai.

---

**End of Document**