import stripe
import csv
from datetime import datetime

# Set your Stripe API Secret Key here
stripe.api_key = "Your_Secret_Key"

# CONFIGURATION
preview_mode = False  # Set to False to perform actual updates
log_file = f"subscription_migration_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Define which prices should be migrated
price_mapping = {
    "price_OLDABC123": "price_NEWABC123",		# Old Price : New Price
    "price_OLDABC456": "price_NEWABC456",		# Old Price : New Price
    "price_OLDABC789": "price_NEWABC789"		# Old Price : New Price
}

# ✅ Migrate only subscriptions in these states
valid_statuses = {"active", "trialing", "past_due", "unpaid"}

# 📦 Fetch subscriptions
subscriptions = stripe.Subscription.list(limit=100)

# 🧾 Open CSV log
with open(log_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Subscription ID", "Customer", "Old Price", "New Price", "Status", "Action Taken"])

    for sub in subscriptions.auto_paging_iter():
        if sub["status"] not in valid_statuses:
            continue

        new_items = []
        has_changes = False

        for item in sub["items"]["data"]:
            old_price = item["price"]["id"]

            if old_price in price_mapping:
                new_price = price_mapping[old_price]
                action = "Would Migrate" if preview_mode else "Migrated"
                print(f"{action} subscription {sub['id']}: {old_price} → {new_price}")

                new_items.append({
                    "id": item["id"],
                    "price": new_price
                })

                writer.writerow([
                    sub["id"],
                    sub["customer"],
                    old_price,
                    new_price,
                    sub["status"],
                    action
                ])
                has_changes = True
            else:
                # Keep the existing item
                new_items.append({
                    "id": item["id"],
                    "price": item["price"]["id"]
                })

        # 🚀 Apply changes only if needed
        if has_changes and not preview_mode:
            stripe.Subscription.modify(
                sub["id"],
                items=new_items,
                proration_behavior="none"
            )

print(f"\n✅ Log saved to {log_file}")
if preview_mode:
    print("🔍 Preview mode ON — no changes made.")
else:
    print("🚀 Migration complete.")
