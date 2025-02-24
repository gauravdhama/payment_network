from collections import defaultdict

from app.models.transaction import Transaction

def calculate_bill(customer_id, start_date, end_date):
    """
    Calculates the bill for a customer with a breakdown of charges by billing codes.
    """
    #... (fetch customer's billing plan)...

    #... (calculate bill based on billing plan)...

    # Generate billing code breakdown
    billing_code_breakdown = defaultdict(lambda: {'amount': 0, 'transactions':})
    transactions = Transaction.query.filter(
        Transaction.customer_id == customer_id,
        Transaction.created_at >= start_date,
        Transaction.created_at <= end_date
    ).all()
    for transaction in transactions:
        billing_code = get_billing_code(transaction.billing_code_id)  # You'll need to implement this function
        billing_code_breakdown[billing_code.code]['amount'] += transaction.amount
        billing_code_breakdown[billing_code.code]['transactions'].append(transaction.id)

    return bill_amount, billing_code_breakdown
