"""Payment processing service"""
from decimal import Decimal
from datetime import datetime
import uuid

class PaymentProcessor:
    def __init__(self, api_key, environment='sandbox'):
        self.api_key = api_key
        self.environment = environment
        self.transactions = {}
    
    def charge_credit_card(self, card_number, amount, currency='USD'):
        """Process a credit card payment"""
        # Validate amount
        if amount <= 0:
            return {'success': False, 'error': 'Invalid amount'}
        
        # Create transaction record
        transaction_id = str(uuid.uuid4())
        
        transaction = {
            'id': transaction_id,
            'type': 'charge',
            'amount': Decimal(str(amount)),
            'currency': currency,
            'card_last_four': card_number[-4:],
            'status': 'pending',
            'timestamp': datetime.utcnow()
        }
        
        self.transactions[transaction_id] = transaction
        
        # Simulate processing
        transaction['status'] = 'completed'
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'amount_charged': float(amount)
        }
    
    def refund_payment(self, transaction_id, amount=None):
        """Issue a refund for a previous transaction"""
        if transaction_id not in self.transactions:
            return {'success': False, 'error': 'Transaction not found'}
        
        original = self.transactions[transaction_id]
        
        if original['status'] != 'completed':
            return {'success': False, 'error': 'Cannot refund incomplete transaction'}
        
        refund_amount = amount if amount else original['amount']
        
        if refund_amount > original['amount']:
            return {'success': False, 'error': 'Refund exceeds original amount'}
        
        refund_id = str(uuid.uuid4())
        
        refund = {
            'id': refund_id,
            'type': 'refund',
            'original_transaction': transaction_id,
            'amount': Decimal(str(refund_amount)),
            'currency': original['currency'],
            'status': 'completed',
            'timestamp': datetime.utcnow()
        }
        
        self.transactions[refund_id] = refund
        
        return {
            'success': True,
            'refund_id': refund_id,
            'amount_refunded': float(refund_amount)
        }
    
    def calculate_processing_fee(self, amount, fee_percentage=2.9, fixed_fee=0.30):
        """Calculate payment processing fees"""
        percentage_fee = Decimal(str(amount)) * Decimal(str(fee_percentage / 100))
        total_fee = percentage_fee + Decimal(str(fixed_fee))
        
        return {
            'amount': float(amount),
            'percentage_fee': float(percentage_fee),
            'fixed_fee': float(fixed_fee),
            'total_fee': float(total_fee),
            'net_amount': float(Decimal(str(amount)) - total_fee)
        }
    
    def create_subscription(self, customer_id, plan_id, billing_cycle='monthly'):
        """Set up a recurring subscription payment"""
        subscription_id = str(uuid.uuid4())
        
        subscription = {
            'id': subscription_id,
            'customer_id': customer_id,
            'plan_id': plan_id,
            'billing_cycle': billing_cycle,
            'status': 'active',
            'created_at': datetime.utcnow(),
            'next_billing_date': self._calculate_next_billing(billing_cycle)
        }
        
        return {
            'success': True,
            'subscription': subscription
        }
    
    def _calculate_next_billing(self, billing_cycle):
        """Calculate the next billing date"""
        from datetime import timedelta
        
        if billing_cycle == 'monthly':
            return datetime.utcnow() + timedelta(days=30)
        elif billing_cycle == 'yearly':
            return datetime.utcnow() + timedelta(days=365)
        else:
            return datetime.utcnow() + timedelta(days=7)
    
    def verify_payment_method(self, card_number, cvv, expiry_date):
        """Verify payment method is valid"""
        # Basic validation
        if len(card_number) < 13 or len(card_number) > 19:
            return {'valid': False, 'error': 'Invalid card number'}
        
        if len(cvv) not in [3, 4]:
            return {'valid': False, 'error': 'Invalid CVV'}
        
        return {'valid': True}
