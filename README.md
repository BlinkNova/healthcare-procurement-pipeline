# Healthcare Procurement Data Ingestion Pipeline

## Overview
This repository contains an automated Python data ingestion pipeline designed to process incoming procurement feeds, enforce data integrity against PostgreSQL reference tables, and handle record routing based on foreign key validation.

## Key Features
- **Data Validation**: Cross-checks incoming `product_id` records against validated products in PostgreSQL.
- **Conditional Routing**:
  - **Valid Records**: Automatically inserted into the `procurement_events` core table.
  - **Invalid Records**: Quarantined into `quarantine_logs` as JSON with detailed error metadata for auditability.
- **Robust Exception Handling**: Prevents pipeline failure when encountering missing foreign key relations or bad data rows.

## Schema Architecture
The database consists of four primary tables:
1. `products`: Reference list of approved healthcare items (`product_id` PRIMARY KEY).
2. `suppliers`: Reference list of approved vendors (`supplier_id` PRIMARY KEY).
3. `procurement_events`: Verified transaction log with foreign key relationships to `products` and `suppliers`.
4. `quarantine_logs`: Audit log storing raw JSON payloads and error messages for flagged records.

## Tech Stack
- **Language**: Python 3.x
- **Database**: PostgreSQL (managed via pgAdmin)
- **Libraries**: `pandas`, `psycopg2`

## How to Run
1. Ensure PostgreSQL is running locally and the database `healthcare_procurement` is created.
2. Run schema setup scripts to create `products`, `suppliers`, `procurement_events`, and `quarantine_logs`.
3. Place `incoming_procurement.csv` in the root directory.
4. Execute the pipeline:
   ```bash
   python app.py
