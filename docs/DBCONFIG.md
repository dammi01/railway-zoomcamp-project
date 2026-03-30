
# Data Warehouse & Schema Specification

## 1\. Physical Storage Layer

  * **Warehouse:** Google BigQuery
  * **Location:** `europe-west3` (Frankfurt)
  * **Table Name:** `railway_data_lake.trains_gold`
  * **Optimization:** BigQuery BI Engine (2GB Reservation)

## 2\. Table Schema (The "Gold" Layer)

We use a flattened schema to maximize performance for Looker Studio. This avoids expensive `JOIN` operations at runtime.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `service_id` | `STRING` | Unique identifier for the train service. |
| `service_date` | `DATE` | **Partitioning Key.** Used for cost-control. |
| `station_name` | `STRING` | The physical station location. |
| `scheduled_arrival` | `TIMESTAMP` | The planned stop time. |
| `actual_arrival` | `TIMESTAMP` | The actual sensor-logged stop time. |
| `delay_seconds` | `INT64` | Calculated difference (Actual - Scheduled). |
| `is_ghost_stop` | `BOOL` | True if scheduled but `actual_arrival` is NULL. |
| `is_cancelled` | `BOOL` | Logical sync flag from service-level logs. |

## 3\. Engineering Decisions

### Partitioning & Sharding

The table is **Partitioned by Day** on the `service_date` column.

> **Why?** Since the dataset contains 22.2M rows, scanning the entire table for a "Last 7 Days" report would be expensive. Partitioning ensures BigQuery only reads the relevant storage buckets, reducing query costs by up to 90%.

### Data Integrity Logic

To handle the "Ghost Stop" identification, the pipeline applies a **Logical Sync**:
$$If \text{ service\_cancelled} = \text{True} \implies \text{all stop\_arrivals} = \text{Cancelled}$$
This prevents the dashboard from showing "Delayed" status for trains that never actually left the yard.

### Sub-Second Interactivity

By using **INT64** for delays and **BOOL** for flags, we reduce the byte-size of each row. Combined with the **BI Engine**, this allows the 22M row table to behave like a 100-row table in the UI.


