import csv
import stripe
import os

# Set your Stripe API Secret Key here
stripe.api_key = "Your_Secret_Key"

input_file = "customers.csv"
output_file = "subscription_counts.csv"
results = []

with open(input_file, mode="r") as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [field.strip().lower().replace(" ", "_") for field in reader.fieldnames]

    for row in reader:
        customer_id = row["customer_id"]
        try:
            subs = stripe.Subscription.list(customer=customer_id, limit=100)
            subscriptions = subs['data']
            count = len(subscriptions)
            statuses = [sub['status'] for sub in subscriptions]
            status_list = ",".join(statuses) if statuses else ""
            print(f"{customer_id}: {count} subscription(s) - {status_list}")
            results.append({
                "customer_id": customer_id,
                "subscription_count": count,
                "statuses": status_list
            })
        except stripe.error.StripeError as e:
            print(f"Error for {customer_id}: {e.user_message or str(e)}")
            results.append({
                "customer_id": customer_id,
                "subscription_count": "ERROR",
                "statuses": "ERROR"
            })

# Write results to output CSV
with open(output_file, mode="w", newline="") as csvfile:
    fieldnames = ["customer_id", "subscription_count", "statuses"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)

print(f"\n✅ Export complete. File saved as: {os.path.abspath(output_file)}")
