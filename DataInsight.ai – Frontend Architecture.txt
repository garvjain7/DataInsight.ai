# DataInsight.ai – Frontend Architecture & Responsibilities

**Document Purpose:** Define the responsibilities, flow, and improvements required in the frontend of DataInsight.ai.

**Important Note:** The existing frontend repository must be updated and improved. A complete rewrite is not allowed.

---

# 1. Frontend Scope

The frontend is responsible for:

* User interaction
* Dataset upload interface
* Displaying job progress
* Rendering analytics and visualizations
* Showing model reports
* Providing chatbot interaction
* Managing dataset history

The frontend is NOT responsible for:

* Running ML training
* Performing ETL
* Generating embeddings
* Business logic decisions

The backend remains the source of truth.

---

# 2. Page Flow Definition

The system follows a job-centric UI model.

## 2.1 Upload Page (`/upload`)

Responsibilities:

* Upload dataset (CSV, Excel, JSON)
* Optional fields:

  * Target column
  * Problem type

These fields are optional.

If provided:

* Sent to backend
* Backend validates and uses them

If not provided:

* Backend auto-detects

On success:

* Backend returns `job_id`
* User redirected to `/job/:job_id`

---

## 2.2 Job Dashboard (`/job/:job_id`)

Responsibilities:

* Poll job status
* Display current stage
* Show progress indicator
* Show failure messages if any

When ETL completes:

Option A: Automatically redirect to Analytics page.

Option B: Show interactive popup:
"ETL Completed. View Analytics?"

Pipeline must continue running in background.

---

## 2.3 Analytics Page (`/job/:job_id/analytics`)

Displays:

* Dataset summary
* Missing values
* Column types
* Graphs and charts
* Class distribution (if classification)

Data fetched from:
`GET /job/:job_id/analytics`

Must only render when state >= ETL_COMPLETED.

---

## 2.4 Report Page (`/job/:job_id/report`)

Displays:

* Model summary
* Performance metrics
* Feature importance
* Structured explanations

Accessible only when state >= REPORT_GENERATED.

---

## 2.5 Chat Page (`/job/:job_id/chat`)

Responsibilities:

* Send user query
* Display AI response
* Show conversation history

Chat interacts only with report embeddings and metadata.

---

## 2.6 Datasets Page (`/datasets`)

Lists all uploaded datasets.

Each dataset card should show:

* Dataset name
* Upload date
* Current status
* Quick metadata summary

Actions:

* View Analytics
* View Report
* Open Chat
* Download Dataset
* Delete (optional)

This ensures persistent visibility.

---

# 3. Refresh Issue

Current Issue:
On browser refresh, user is redirected to login. That is vulnerable (fix that)

Refresh must NOT log user out unless token expired. it just refresh the same page, and content must not lost

---

# 4. Performance Optimization Strategy

Current Issue:
Frontend loads slowly.

Required Improvements:

## 4.1 Code Splitting

* Use React.lazy for route-based loading
* Load Analytics and Chat only when needed

## 4.2 Bundle Optimization

* Remove unused dependencies
* Use production build
* Analyze bundle using build analyzer

## 4.3 Lazy Load Heavy Libraries

* Chart libraries must load only on analytics page

## 4.4 API Optimization

* Avoid multiple unnecessary API calls on mount
* Poll intelligently (e.g., every 3–5 seconds)

## 4.5 Memoization

* Use React.memo
* Use useMemo and useCallback where needed

## 4.6 Caching

* Cache analytics after first load
* Avoid refetching unchanged data

---

# 5. State Management Rules

* Backend is source of truth
* Never assume stage completion
* Disable buttons when stage incomplete
* Always handle FAILED state

Example:

if (job.status !== "REPORT_GENERATED") {
disableReportAccess();
}

---

# 6. UI Design Principles

* Job-centric routing
* Progressive stage disclosure
* Non-blocking pipeline
* Clear loading indicators
* Clear failure messages
* Clean integration into existing repository

---

# 7. Future Improvements

* WebSocket-based real-time updates
* Multi-job dashboard analytics
* User history tracking
* Improved error visualization

---

**End of Frontend Architecture Document**
