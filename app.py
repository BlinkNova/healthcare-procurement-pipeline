import pandas as pd
import psycopg2

def run_ingestion():
    # 1. Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname="healthcare_procurement",
        user="postgres",
        password="novaDE2026",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # 2. Fetch existing valid product IDs from PostgreSQL
    cursor.execute("SELECT product_id FROM products;")
    valid_products = {row[0] for row in cursor.fetchall()}

    # 3. Read incoming raw CSV procurement feed
    df = pd.read_csv("incoming_procurement.csv")

    # 4. Process each row: validate against existing products and route
    for _, row in df.iterrows():
        if row['product_id'] in valid_products:
            # Route VALID rows to procurement_events table
            insert_query = """
                INSERT INTO procurement_events 
                (event_id, supplier_id, product_id, purchase_date, quantity, unit_price_gbp, line_total_gbp, buying_org, source_channel)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, tuple(row))
            print(f"[SUCCESS] Routed to procurement_events: {row['event_id']}")
        else:
            # Route INVALID rows to quarantine_logs table
            quarantine_query = """
                INSERT INTO quarantine_logs 
                (source_file, raw_data_json, error_message)
                VALUES (%s, %s, %s);
            """
            raw_json = row.to_json()
            error_msg = f"Foreign Key Error: product_id '{row['product_id']}' does not exist in products table."
            cursor.execute(quarantine_query, ("incoming_procurement.csv", raw_json, error_msg))
            print(f"[WARNING] Routed to quarantine_logs: {row['event_id']} (Invalid product_id: {row['product_id']})")

    conn.commit()
    cursor.close()
    conn.close()
    print("\nIngestion pipeline complete!")

if __name__ == "__main__":
    run_ingestion()
