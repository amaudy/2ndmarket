erDiagram
    django_User {
        int id PK
        string username
        string password
        string email
        string first_name
        string last_name
        boolean is_active
        boolean is_staff
        boolean is_superuser
        datetime last_login
        datetime date_joined
    }

    UserProfile {
        int id PK
        int user_id FK "OneToOne"
        string phone_number
        string address
        string avatar
        json email_preferences
        datetime created_at
        datetime updated_at
    }
    
    MAIN_CATEGORY {
        int id PK
        string name
        string slug
        boolean is_active
        int display_order
        datetime created_at
        datetime updated_at
    }

    SUB_CATEGORY {
        int id PK
        int main_category_id FK
        string name
        string slug
        boolean is_active
        int display_order
        datetime created_at
        datetime updated_at
    }

    CATEGORY_ITEM {
        int id PK
        int sub_category_id FK
        string name
        string slug
        boolean is_active
        int display_order
        datetime created_at
        datetime updated_at
    }
    
    PRODUCT_LISTING {
        int id PK
        int seller_id FK
        int category_item_id FK
        string title
        text description
        decimal price
        string condition
        string brand
        boolean is_available
        string status
        int view_count
        datetime last_viewed_at
        datetime created_at
        datetime updated_at
    }
    
    ORDER {
        int id PK
        int buyer_id FK
        int listing_id FK
        decimal total_amount
        string status
        datetime order_date
        string payment_status
        string stripe_payment_intent_id
        string stripe_customer_id
        boolean is_paid
        datetime paid_at
        json status_history
        datetime last_status_update
    }
    
    DELIVERY {
        int id PK
        int order_id FK
        string tracking_number
        string delivery_provider
        string shipping_address
        string status
        json tracking_history
        datetime estimated_delivery
        datetime actual_delivery
        datetime last_update
    }
    
    PRODUCT_IMAGES {
        int id PK
        int listing_id FK
        string image_url
        boolean is_primary
    }

    CATEGORY_ATTRIBUTES {
        int id PK
        int main_category_id FK
        string name
        string type
        boolean is_required
        string validation_rules
    }
    
    PRODUCT_ATTRIBUTE_VALUES {
        int id PK
        int listing_id FK
        int attribute_id FK
        string value
    }

    PRODUCT_LIKES {
        int id PK
        int listing_id FK
        int user_id FK
        datetime created_at
    }

    PRODUCT_VIEWS {
        int id PK
        int listing_id FK
        int user_id FK
        datetime viewed_at
        string ip_address
    }

    REVIEWS {
        int id PK
        int user_id FK
        int listing_id FK
        text content
        int rating
        boolean is_edited
        datetime edited_at
        datetime created_at
        datetime updated_at
    }

    NOTIFICATIONS {
        int id PK
        int user_id FK
        string type
        string message
        json data
        boolean is_read
        datetime created_at
    }

    MESSAGES {
        int id PK
        int order_id FK
        int sender_id FK
        int receiver_id FK
        text content
        boolean is_read
        datetime created_at
        datetime updated_at
    }

    django_User ||--|| UserProfile : "has"
    django_User ||--o{ PRODUCT_LISTING : "lists"
    django_User ||--o{ ORDER : "places"
    django_User ||--o{ PRODUCT_LIKES : "likes"
    django_User ||--o{ PRODUCT_VIEWS : "views"
    django_User ||--o{ REVIEWS : "writes"
    django_User ||--o{ NOTIFICATIONS : "receives"
    PRODUCT_LISTING ||--o{ REVIEWS : "has"
    
    MAIN_CATEGORY ||--o{ SUB_CATEGORY : "contains"
    SUB_CATEGORY ||--o{ CATEGORY_ITEM : "contains"
    CATEGORY_ITEM ||--o{ PRODUCT_LISTING : "has products"
    
    MAIN_CATEGORY ||--o{ CATEGORY_ATTRIBUTES : "has"
    PRODUCT_LISTING ||--o{ PRODUCT_IMAGES : "has"
    PRODUCT_LISTING ||--o{ ORDER : "included_in"
    PRODUCT_LISTING ||--o{ PRODUCT_ATTRIBUTE_VALUES : "has"
    CATEGORY_ATTRIBUTES ||--o{ PRODUCT_ATTRIBUTE_VALUES : "defines"
    ORDER ||--|| DELIVERY : "has"
    PRODUCT_LISTING ||--o{ PRODUCT_LIKES : "receives"
    PRODUCT_LISTING ||--o{ PRODUCT_VIEWS : "receives"
    ORDER ||--o{ PAYMENT_TRANSACTION : "has"
    ORDER ||--o{ MESSAGES : "has"
    django_User ||--o{ MESSAGES : "sends"