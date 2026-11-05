---
name: refunds
description: How much to refund and how. Use whenever a customer asks for their money back, a return, or a refund on beans, equipment or a subscription box.
---
# Refunds

Use the script to work out the amount; never work it out in your head. Run:

    python3 .claude/skills/refunds/scripts/refund.py --price PRICE --days DAYS_SINCE_DELIVERY --opened yes|no

It prints the refund to the original payment, the store-credit option, and which rule applied.

## The rules the script applies
- Unopened, within 30 days of delivery: full refund to the original payment.
- Opened, within 14 days of delivery: 50% back to the original payment, or 100% as store credit. The customer chooses.
- Opened, 15–30 days after delivery: store credit only, 50%.
- More than 30 days after delivery: store credit only, 25%, and only once per customer per year.
- Shipping ($6.50 standard) is refunded only when the mistake was ours (wrong item, damaged, lost).

## Steps
1. Find the price, the delivery date and whether the bag or box was opened. If any of the three is missing, ask for it; don't guess.
2. Run the script with those numbers.
3. Tell the customer the options the script printed, in one short paragraph, with the amounts.
4. Refunds reach the customer's bank in 3–5 working days. Store credit is added to their account at once.
5. Equipment (grinders, kettles, scales) must be returned unused in its box for a refund; send the customer the returns address only after they confirm.

## Never
- Never refund more than the script prints, even if the customer asks nicely. Offer LATE10 or a free sample bag instead if they are unhappy.
- Never refund a gift card purchase: see gift cards.
