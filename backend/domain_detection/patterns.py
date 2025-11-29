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
    """Collection of all domain patterns and utility methods."""

    # MEDIA/ENTERTAINMENT PATTERNS
    MEDIA = DomainPattern(
        name="media",
        keywords={
            'track', 'track_id', 'track_name', 'track_number', 'track_popularity', 'track_duration',
            'artist', 'artist_id', 'artist_name', 'artist_popularity', 'artist_followers', 'artist_genres',
            'album', 'album_id', 'album_name', 'album_type', 'album_release_date', 'album_total_tracks',
            'genre', 'genres',
            'explicit',
            'popularity', 'followers',
            'duration', 'duration_min', 'duration_ms'
        },
        data_patterns=set(),
        relationships=[
            ('track', 'artist'),
            ('track', 'album'),
            ('artist', 'genre'),
        ],
        weight=1.0
    )

    # CUSTOMER/CRM PATTERNS  
    CUSTOMER = DomainPattern(
        name="customer",
        keywords={
            'customer', 'customer_id', 'customer_name',
            'name', 'email', 'email_address',
            'age', 'country', 'city', 'phone',
            'signup_date', 'registration_date', 'created_date',
            'total_purchases', 'purchase_count', 'order_count',
            'total_spent', 'total_revenue', 'lifetime_value', 'ltv',
            'last_purchase', 'last_order_date',
            'status', 'segment', 'tier',
            'subscription', 'plan'
        },
        data_patterns=set(),
        relationships=[
            ('customer', 'purchase'),
            ('customer', 'order'),
        ],
        weight=1.1
    )


    # E-COMMERCE PATTERNS
    ECOMMERCE = DomainPattern(
        name="e-commerce",
        keywords={
            # Product identity
            'product', 'product_id', 'product_name',

            # Pricing and discounts
            'price', 'discounted_price', 'actual_price', 'discount', 'discount_percentage',

            # Categorization
            'category',

            # Ratings and reviews
            'rating', 'rating_count',
            'review', 'review_id', 'review_title', 'review_content',

            # Users / customers
            'user', 'user_id', 'user_name',

            # Core e-commerce actions
            'order', 'cart', 'checkout', 'purchase', 'transaction',

            # Fulfillment
            'shipping', 'delivery'
        },
        data_patterns={
            r'\$\d+\.\d{2}',          # Price format
            r'USD|EUR|GBP|INR',       # Currency codes
            r'SKU-\d+',               # SKU format
        },
        relationships=[
            ('order', 'customer'),
            ('order', 'product'),
            ('customer', 'review'),
        ],
        weight=1.2
    )
    # FINANCE PATTERNS
    FINANCE = DomainPattern(
        name="finance",
        keywords={
            'account', 'balance', 'credit', 'debit', 'transaction',
            'payment', 'deposit', 'withdrawal', 'transfer',
            'interest', 'principal', 'apr', 'rate',
            'loan', 'mortgage', 'investment', 'portfolio',
            'bank', 'branch', 'routing', 'swift',
            'currency', 'exchange', 'forex',
            'statement', 'ledger', 'journal',
            'revenue', 'expense', 'profit', 'loss',
            'asset', 'liability', 'equity',
            'invoice', 'receipt', 'voucher'
        },
        data_patterns={
            r'\$\d{1,3}(,\d{3})*\.\d{2}',  # Money format
            r'[A-Z]{3}',                  # Currency codes
        },
        relationships=[
            ('account', 'transaction'),
            ('loan', 'payment'),
        ],
        weight=1.1
    )

    # CRM PATTERNS
    CRM = DomainPattern(
        name="crm",
        keywords={
            'customer', 'client', 'contact', 'lead', 'prospect',
            'account', 'opportunity', 'deal', 'pipeline',
            'campaign', 'marketing', 'email', 'call', 'meeting',
            'stage', 'status', 'priority', 'owner',
            'activity', 'task', 'note', 'comment',
            'first_name', 'last_name', 'full_name',
            'email_address', 'phone', 'mobile',
            'company', 'organization', 'title', 'role',
            'source', 'channel', 'referral',
            'conversion', 'qualification', 'closed_won', 'closed_lost'
        },
        data_patterns=set(),
        relationships=[
            ('account', 'contact'),
            ('deal', 'contact'),
        ],
        weight=1.0
    )

    # HEALTHCARE PATTERNS
    HEALTHCARE = DomainPattern(
        name="healthcare",
        keywords={
            'patient', 'diagnosis', 'treatment', 'medication',
            'prescription', 'dosage', 'pharmacy',
            'doctor', 'physician', 'nurse', 'provider',
            'hospital', 'clinic', 'facility',
            'appointment', 'visit', 'admission', 'discharge',
            'symptom', 'condition', 'disease', 'disorder',
            'lab', 'test', 'result', 'value',
            'insurance', 'claim', 'coverage', 'copay',
            'vital', 'blood_pressure', 'heart_rate', 'temperature',
            'medical_record', 'chart', 'history'
        },
        data_patterns=set(),
        relationships=[
            ('patient', 'appointment'),
            ('patient', 'diagnosis'),
        ],
        weight=1.0
    )

    # LOGISTICS PATTERNS
    LOGISTICS = DomainPattern(
        name="logistics",
        keywords={
            'shipment', 'tracking', 'carrier', 'delivery',
            'warehouse', 'inventory', 'stock', 'storage',
            'pickup', 'dropoff', 'route', 'driver',
            'package', 'parcel', 'container', 'pallet',
            'weight', 'dimension', 'volume', 'cubic',
            'origin', 'destination', 'transit', 'eta',
            'freight', 'cargo', 'shipping', 'transport',
            'customs', 'clearance', 'duty', 'tariff',
            'manifest', 'bill_of_lading', 'invoice'
        },
        data_patterns=set(),
        relationships=[
            ('shipment', 'carrier'),
            ('shipment', 'warehouse'),
        ],
        weight=1.0
    )

    # HR PATTERNS
    HR = DomainPattern(
        name="hr",
        keywords={
            'employee', 'staff', 'personnel', 'worker',
            'hire', 'onboard', 'termination', 'resignation',
            'department', 'position', 'title', 'role',
            'salary', 'wage', 'compensation', 'bonus',
            'benefits', 'insurance', 'retirement', '401k',
            'performance', 'review', 'evaluation', 'rating',
            'attendance', 'leave', 'vacation', 'sick_day',
            'timesheet', 'hours', 'overtime', 'shift',
            'training', 'certification', 'skill',
            'manager', 'supervisor', 'direct_report'
        },
        data_patterns=set(),
        relationships=[
            ('employee', 'department'),
            ('employee', 'manager'),
        ],
        weight=1.0
    )

    # MARKETING PATTERNS
    MARKETING = DomainPattern(
        name="marketing",
        keywords={
            'campaign', 'ad', 'advertisement', 'promotion',
            'click', 'impression', 'view', 'engagement',
            'ctr', 'cpc', 'cpm', 'roas', 'roi',
            'conversion', 'funnel', 'landing_page',
            'email', 'newsletter', 'blast', 'drip',
            'social', 'facebook', 'instagram', 'twitter',
            'audience', 'segment', 'demographic', 'target',
            'keyword', 'search', 'seo', 'sem',
            'content', 'blog', 'article', 'post',
            'analytics', 'metrics', 'kpi'
        },
        data_patterns=set(),
        relationships=[
            ('campaign', 'audience'),
            ('campaign', 'channel'),
        ],
        weight=1.0
    )

    # SAAS PATTERNS
    SAAS = DomainPattern(
        name="saas",
        keywords={
            'subscription', 'plan', 'tier', 'license',
            'user', 'account', 'tenant', 'workspace',
            'signup', 'trial', 'activation', 'churn',
            'mrr', 'arr', 'ltv', 'cac',
            'feature', 'usage', 'quota', 'limit',
            'api', 'endpoint', 'request', 'response',
            'integration', 'webhook', 'oauth',
            'billing', 'invoice', 'payment_method',
            'upgrade', 'downgrade', 'cancel', 'renewal'
        },
        data_patterns=set(),
        relationships=[
            ('account', 'subscription'),
            ('user', 'workspace'),
        ],
        weight=1.0
    )

    @classmethod
    def get_all_patterns(cls) -> Dict[str, DomainPattern]:
        """Return all domain patterns as a dictionary."""
        return {
            'e-commerce': cls.ECOMMERCE,
            'finance': cls.FINANCE,
            'crm': cls.CRM,
            'healthcare': cls.HEALTHCARE,
            'logistics': cls.LOGISTICS,
            'hr': cls.HR,
            'marketing': cls.MARKETING,
            'customer': cls.CUSTOMER,
            'media': cls.MEDIA,
            'saas': cls.SAAS,

        }
