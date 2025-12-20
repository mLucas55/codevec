from decimal import Decimal
from typing import Dict, List
import datetime

class PaymentProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.transactions = []
    
    def process_credit_card_payment(self, amount: Decimal, card_number: str, cvv: str) -> Dict:
        """Process a credit card payment and return transaction details"""
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        
        # Simulate payment processing
        transaction = {
            'amount': float(amount),
            'card_last_four': card_number[-4:],
            'status': 'approved',
            'timestamp': datetime.datetime.now().isoformat(),
            'transaction_id': f"TXN-{len(self.transactions) + 1:06d}"
        }
        self.transactions.append(transaction)
        return transaction
    
    def refund_payment(self, transaction_id: str, amount: Decimal) -> bool:
        """Issue a refund for a previous transaction"""
        for txn in self.transactions:
            if txn['transaction_id'] == transaction_id:
                print(f"Refunding {amount} for transaction {transaction_id}")
                return True
        return False

def calculate_transaction_fee(amount: Decimal, fee_percentage: float = 2.9) -> Decimal:
    """Calculate the transaction fee based on amount and percentage"""
    return amount * Decimal(fee_percentage / 100)

def verify_payment_address(street: str, city: str, zip_code: str) -> bool:
    """Verify that a payment address is valid"""
    if not street or not city or not zip_code:
        return False
    
    # Basic validation
    if len(zip_code) != 5:
        return False
    
    return True

def generate_invoice(customer_name: str, items: List[Dict], tax_rate: float = 0.08) -> Dict:
    """Generate an invoice with line items and calculate total with tax"""
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    return {
        'customer': customer_name,
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'date': datetime.datetime.now().isoformat()
    }
