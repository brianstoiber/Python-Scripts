import stripe
import csv

# Set your Stripe API Secret Key here
stripe.api_key = "your_secret_key_here"

# Define the specific account ID
TARGET_ACCOUNT_ID = "acct_1MRgjXDHUKyS7Sl8"

# Output file
OUTPUT_FILE = "customers_export.csv"

def fetch_all_customers():
    """
    Retrieves all customers from the specified Stripe account and returns their data.
    """
    try:
        customers = stripe.Customer.list(limit=100, stripe_account=TARGET_ACCOUNT_ID)  # Fetch customers
        all_customers = []

        for customer in customers.auto_paging_iter():
            customer_data = {
                "Customer ID": customer.id,
                "Email": customer.email or "N/A",
                "Created": customer.created,
                "Name": customer.name or "N/A",
                "Metadata": customer.metadata or {},  # Store metadata as a dictionary
            }
            all_customers.append(customer_data)

        return all_customers

    except stripe.error.StripeError as e:
        print(f"❌ Stripe API error while retrieving customers: {e}")
        return []

def export_to_csv(customers):
    """
    Exports customer data, including all metadata keys/values, to a CSV file.
    """
    if not customers:
        print("No customer data found. Exiting...")
        return

    # Collect all unique metadata keys from customers
    metadata_keys = set()
    for customer in customers:
        metadata_keys.update(customer["Metadata"].keys())

    # Define CSV column headers
    headers = ["Customer ID", "Email", "Created", "Name"] + sorted(metadata_keys)

    # Write to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for customer in customers:
            row = {
                "Customer ID": customer["Customer ID"],
                "Email": customer["Email"],
                "Created": customer["Created"],
                "Name": customer["Name"],
            }
            # Add metadata values, leaving empty if the key doesn't exist for a customer
            for key in metadata_keys:
                row[key] = customer["Metadata"].get(key, "")

            writer.writerow(row)

    print(f"✅ Customer data exported successfully to {OUTPUT_FILE}")

# Run the script
if __name__ == "__main__":
    customers = fetch_all_customers()
    export_to_csv(customers)
