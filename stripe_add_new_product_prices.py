import stripe

# Set your Stripe API Secret Key here
stripe.api_key = "Your_Secret_Key"

# Product and common config
product_id = "prod_ABC123"
amount_cents = 3800  # $38.00
currency = "usd"
nickname_base = "Price description"
tax_code = "PM020760"
tax_behavior = "exclusive"
metadata = {"TaxCode": tax_code}

# 1. One-time purchase (no recurring)
one_time = stripe.Price.create(
    unit_amount=amount_cents,
    currency=currency,
    product=product_id,
    nickname=f"{nickname_base} - One-time",
    metadata=metadata,
    tax_behavior=tax_behavior
)

# 2. Monthly subscription
monthly = stripe.Price.create(
    unit_amount=amount_cents,
    currency=currency,
    product=product_id,
    nickname=f"{nickname_base} - Monthly",
    metadata=metadata,
    tax_behavior=tax_behavior,
    recurring={"interval": "month"}
)

# 3. Every 2 months
bimonthly = stripe.Price.create(
    unit_amount=amount_cents,
    currency=currency,
    product=product_id,
    nickname=f"{nickname_base} - Every 2 months",
    metadata=metadata,
    tax_behavior=tax_behavior,
    recurring={"interval": "month", "interval_count": 2}
)

# 4. Every 3 months
quarterly = stripe.Price.create(
    unit_amount=amount_cents,
    currency=currency,
    product=product_id,
    nickname=f"{nickname_base} - Every 3 months",
    metadata=metadata,
    tax_behavior=tax_behavior,
    recurring={"interval": "month", "interval_count": 3}
)

# Set monthly subscription as default price
stripe.Product.modify(
    product_id,
    default_price=monthly.id
)


# Print confirmation
print("Prices created:")
print(f"✅ One-time:      {one_time.id}")
print(f"✅ Monthly:       {monthly.id}")
print(f"✅ Every 2 months:{bimonthly.id}")
print(f"✅ Every 3 months:{quarterly.id}")
print(f"✅ Set {monthly.id} as the default price for product {product_id}")
