"""
Domain Pattern Library - Business Domain Detection Patterns
Contains keyword patterns and rules for identifying different business domains.
"""

from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class DomainPattern:
    """Pattern definition for a business domain."""
    name: str
    keywords: Set[str]
    data_patterns: Set[str]
    relationships: List[tuple]
    weight: float = 1.0


class DomainPatterns:
    """
    Library of domain-specific patterns for automatic classification.
    Production-ready domain detection patterns.
    """
    
    # E-COMMERCE PATTERNS
    ECOMMERCE = DomainPattern(
        name="e-commerce",
        keywords={
            'product', 'item', 'sku', 'catalog', 'inventory',
            'price', 'cost', 'retail', 'wholesale', 'discount',
            'category', 'brand', 'manufacturer', 'model',
            'order', 'cart', 'checkout', 'purchase', 'transaction',
            'quantity', 'qty', 'amount', 'total', 'subtotal',
            'shipping', 'delivery', 'fulfillment',
            'customer', 'buyer', 'shopper', 'user',
            'revenue', 'sales', 'conversion', 'commission'
        },
        data_patterns={
            'currency', 'product_id', 'order_id', 'sku_format',
            'price_format', 'quantity_numeric'
        },
        relationships=[
            ('order_id', 'product_id'),
            ('customer_id', 'order_id'),
            ('product_id', 'price')
        ],
        weight=1.0
    )
    
    # FINANCE PATTERNS
    FINANCE = DomainPattern(
        name="finance",
        keywords={
            'transaction', 'payment', 'transfer', 'withdrawal',
            'deposit', 'balance', 'amount', 'debit', 'credit',
            'account', 'portfolio', 'investment', 'loan',
            'interest', 'rate', 'apr', 'yield', 'dividend',
            'bank', 'branch', 'routing', 'swift', 'iban',
            'checking', 'savings', 'statement',
            'revenue', 'expense', 'profit', 'loss', 'equity',
            'asset', 'liability', 'cash_flow'
        },
        data_patterns={
            'currency', 'account_number', 'transaction_id',
            'decimal_precision', 'balance_format'
        },
        relationships=[
            ('account_id', 'transaction_id'),
            ('account_id', 'balance'),
            ('transaction_id', 'amount')
        ],
        weight=1.0
    )
    
    # CRM PATTERNS
    CRM = DomainPattern(
        name="crm",
        keywords={
            'customer', 'client', 'contact', 'prospect', 'lead',
            'account', 'company', 'organization',
            'email', 'phone', 'mobile', 'address', 'communication',
            'call', 'meeting', 'appointment', 'interaction',
            'opportunity', 'deal', 'pipeline', 'stage', 'funnel',
            'quote', 'proposal', 'contract', 'close',
            'score', 'rating', 'status', 'priority', 'segment',
            'lifetime_value', 'ltv', 'churn', 'retention'
        },
        data_patterns={
            'email_format', 'phone_format', 'contact_id',
            'lead_score', 'deal_value'
        },
        relationships=[
            ('customer_id', 'contact_id'),
            ('lead_id', 'opportunity_id'),
            ('account_id', 'deal_id')
        ],
        weight=1.0
    )
    
    # HEALTHCARE PATTERNS
    HEALTHCARE = DomainPattern(
        name="healthcare",
        keywords={
            'patient', 'medical', 'health', 'clinical',
            'diagnosis', 'symptom', 'condition', 'disease',
            'prescription', 'medication', 'drug', 'dosage',
            'treatment', 'procedure', 'surgery', 'therapy',
            'doctor', 'physician', 'nurse', 'provider',
            'specialist', 'practitioner',
            'hospital', 'clinic', 'ward', 'department',
            'admission', 'discharge', 'appointment', 'visit',
            'record', 'chart', 'lab', 'test', 'result',
            'vital', 'blood_pressure', 'temperature'
        },
        data_patterns={
            'patient_id', 'medical_record_number', 'icd_code',
            'medication_name', 'date_of_birth'
        },
        relationships=[
            ('patient_id', 'diagnosis_id'),
            ('patient_id', 'prescription_id'),
            ('doctor_id', 'patient_id')
        ],
        weight=1.0
    )
    
    # HR PATTERNS
    HR = DomainPattern(
        name="hr",
        keywords={
            'employee', 'staff', 'worker', 'personnel',
            'hire', 'termination', 'onboard', 'offboard',
            'salary', 'wage', 'compensation', 'bonus', 'benefits',
            'payroll', 'pay', 'hourly', 'annual',
            'department', 'division', 'team', 'manager',
            'supervisor', 'position', 'title', 'role',
            'performance', 'review', 'evaluation', 'rating',
            'goal', 'objective', 'feedback',
            'attendance', 'leave', 'vacation', 'sick', 'pto',
            'hours', 'overtime', 'timesheet'
        },
        data_patterns={
            'employee_id', 'ssn_format', 'salary_numeric',
            'hire_date', 'department_code'
        },
        relationships=[
            ('employee_id', 'department_id'),
            ('employee_id', 'manager_id'),
            ('employee_id', 'salary')
        ],
        weight=1.0
    )
    
    # LOGISTICS PATTERNS
    LOGISTICS = DomainPattern(
        name="logistics",
        keywords={
            'shipment', 'shipping', 'delivery', 'freight',
            'tracking', 'carrier', 'courier',
            'warehouse', 'inventory', 'stock', 'storage',
            'bin', 'location', 'facility',
            'vehicle', 'truck', 'route', 'trip', 'driver',
            'transport', 'dispatch',
            'status', 'eta', 'arrival', 'departure',
            'in_transit', 'delivered', 'pending',
            'origin', 'destination', 'address', 'zip',
            'city', 'state', 'country'
        },
        data_patterns={
            'tracking_number', 'warehouse_id', 'address_format',
            'shipment_id', 'weight_numeric'
        },
        relationships=[
            ('shipment_id', 'tracking_number'),
            ('warehouse_id', 'inventory_id'),
            ('order_id', 'shipment_id')
        ],
        weight=1.0
    )
    
    # MARKETING PATTERNS
    MARKETING = DomainPattern(
        name="marketing",
        keywords={
            'campaign', 'marketing', 'promotion', 'advertisement',
            'ad', 'creative', 'channel', 'medium',
            'impression', 'click', 'conversion', 'ctr', 'roi',
            'engagement', 'reach', 'frequency', 'bounce',
            'email', 'social', 'website', 'landing_page',
            'seo', 'sem', 'ppc', 'organic',
            'content', 'post', 'article', 'blog', 'video',
            'image', 'banner', 'newsletter',
            'audience', 'segment', 'target', 'demographic',
            'behavior', 'persona'
        },
        data_patterns={
            'campaign_id', 'click_rate', 'conversion_rate',
            'email_format', 'url_format'
        },
        relationships=[
            ('campaign_id', 'impression_count'),
            ('campaign_id', 'click_count'),
            ('email_id', 'open_rate')
        ],
        weight=1.0
    )
    
    @classmethod
    def get_all_domains(cls) -> List[DomainPattern]:
        """Get list of all domain patterns."""
        return [
            cls.ECOMMERCE,
            cls.FINANCE,
            cls.CRM,
            cls.HEALTHCARE,
            cls.HR,
            cls.LOGISTICS,
            cls.MARKETING
        ]
    
    @classmethod
    def get_domain_by_name(cls, name: str) -> DomainPattern:
        """Get a specific domain pattern by name."""
        domains = {d.name: d for d in cls.get_all_domains()}
        return domains.get(name.lower())
