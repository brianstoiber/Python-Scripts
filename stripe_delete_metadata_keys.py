import stripe
import os

# Set your Stripe API Secret Key 
stripe.api_key = "Your_Secret_Key"

# Define the specific account ID
TARGET_ACCOUNT_ID = "acct_1234567890"

# Define the audit log file path
LOG_FILE = "audit.txt"

def log_message(message):
    """Logs messages to both the console and audit.txt file."""
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

def remove_metadata_keys(customer_id):
    """
    Removes the specified metadata keys from a given customer in Stripe and logs the action.
    """
    try:
        # Remove metadata fields by setting them to ""
        stripe.Customer.modify(
            customer_id,
            metadata={
                "Address_Country": "",
                "Address_PostalCode": ""
            }
        )
        log_message(f" Successfully removed metadata keys from customer {customer_id}.")

    except stripe.error.StripeError as e:
        log_message(f" Stripe API error for customer {customer_id}: {e}")

def process_all_customers():
    """
    Retrieves and processes all customers under the specified Stripe account.
    """
    log_message(f"\n--- Processing started for account {TARGET_ACCOUNT_ID} ---\n")

    try:
        customers = stripe.Customer.list(limit=100, stripe_account=TARGET_ACCOUNT_ID)  # Fetch customers
        updated_count = 0

        for customer in customers.auto_paging_iter():
            # Check if customer has metadata fields to remove
            metadata = customer.metadata or {}
            keys_to_remove = ["Address_Country", "Address_PostalCode"]
            has_keys = any(key in metadata for key in keys_to_remove)

            if has_keys:
                remove_metadata_keys(customer.id)
                updated_count += 1

        log_message(f"\n--- Processing completed: {updated_count} customers updated in account {TARGET_ACCOUNT_ID}. ---\n")

    except stripe.error.StripeError as e:
        log_message(f" Stripe API error while retrieving customers: {e}")

# Run the script
if __name__ == "__main__":
    process_all_customers()
