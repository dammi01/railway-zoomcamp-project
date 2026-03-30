
***

# Dutch Railway (NS) Reliability Pipeline: Solving the 22M Row Blind Spot

## 📖 Project Narrative: From Chaos to Gold
The Dutch Railway (NS) generates millions of data points daily. Before this project, these logs were a "Black Box." Leaders knew trains were late but could not identify **"Ghost Stops"**—instances where trains are scheduled but fail to stop. Silent failures hurt reputation more than public delays. 

We processed the full **22.2 million records** of the 2024-2025 operational reality to identify the specific **391 stations** requiring immediate technical intervention. This project moves the NS from "guessing" to "knowing."

## 📊 Strategic Insights (The Black Hole Audit)
Our "Gold Layer" analysis revealed critical operational gaps:
* **The Network Ghost Rate:** Identified a **0.03% failure rate**, representing **748,221 "Ghost Stops."**
* [cite_start]**Systemic Failure Hubs:** Utrecht Centraal (20,649 failures) and 's-Hertogenbosch (15,509 failures) are the primary pressure points[cite: 82].
* [cite_start]**The Smoking Gun:** We proved that last-minute **Platform Changes** carry a **220% departure delay penalty** compared to original platform assignments[cite: 108].
* [cite_start]**Operator Performance:** While **NS** and **RRReis** maintain high punctuality, international services like **Eu Sleeper** show arrival delays exceeding **9 minutes** during peak hours[cite: 106].

## 🛠️ Tech Stack & Architecture
* **Orchestration:** **Kestra** (Automates lifecycle and schema enforcement).
* **Data Lake:** **Google Cloud Storage (GCS)**.
* **Processing:** **DuckDB** (Cleans 22M rows at 10x traditional speed).
* **Warehouse:** **BigQuery + BI Engine** (Sub-second query performance).
* **Visualization:** **Looker Studio**.

## 🏗️ Technical Challenges & Solutions

### 1. The 22M Row Browser Bottleneck
* **The Challenge:** Loading 22.2 million records directly into a dashboard causes significant latency and frequent crashes.
* **The Solution:** Implemented **BigQuery BI Engine** with a **2GB memory reservation**. This creates an in-memory acceleration layer.
* **The Result:** Dashboard interaction latency dropped from 15+ seconds to **under 2 seconds**.

### 2. Handling "Ghost" Logic (The Evans Fix)
* **The Challenge:** Raw logs often showed a service as "Active" even when the station stop was cancelled.
* **The Solution:** Engineered a **Logical Cancellation Sync** during the DuckDB transformation phase.
* **The Logic:** If `service_completely_cancelled` is True, the pipeline forces all child `stop_arrival_cancelled` flags to True, ensuring 100% data integrity.

### 3. Cost-Efficient Regional Ingestion
* **The Challenge:** Moving 22M rows across cloud regions triggers high egress costs.
* **The Solution:** Unified the stack in **europe-west3 (Frankfurt)**.
* **The Result:** Achieved a total ingestion-to-warehouse time of **13 seconds** with zero data egress fees.

## ⚖️ Data Engineering Fundamentals
* **Idempotency:** Every Kestra run uses a `LoadFromGcs` task with a `WRITE_TRUNCATE` disposition. Safe retries never duplicate data.
* **Partitioning:** The "Gold" table is **partitioned by `service_date`** and **clustered by `station_name`**. This ensures we only scan necessary shards, keeping BigQuery costs near zero.
* **Network Stability:** The pipeline utilizes **IPv4 explicit binding** for local-to-cloud communication to prevent handshake failures.

## 🚀 How to Run
1.  **Clone the repo.**
2.  **Add your GCP Service Account Key** to the `/orchestration` secrets.
3.  **Run the Kestra flow:**
    `kestra flow resume ns_railway_pipeline`

## 📊 Live Dashboard
[**View the NS 2025 Strategic Reliability Dashboard**](https://lookerstudio.google.com/s/tuGDM5JkYqs)

***

