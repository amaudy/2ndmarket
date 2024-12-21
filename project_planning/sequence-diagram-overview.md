


```
sequenceDiagram
    participant Seller
    participant Marketplace
    participant Buyer
    participant Delivery

    Note over Seller,Marketplace: Product Listing Phase
    Seller->>Marketplace: Create product listing
    Marketplace->>Marketplace: Validate listing
    Marketplace-->>Seller: Confirm listing created
    
    Note over Marketplace,Buyer: Shopping Phase
    Buyer->>Marketplace: Browse listings
    Marketplace-->>Buyer: Display product details
    Buyer->>Marketplace: Select product
    Buyer->>Marketplace: Make payment
    Marketplace-->>Seller: Notify new order
    Marketplace-->>Buyer: Confirm order

    Note over Seller,Delivery: Shipping Phase
    Seller->>Delivery: Request pickup
    Delivery-->>Seller: Confirm pickup schedule
    Delivery->>Delivery: Transport package
    Delivery->>Buyer: Deliver package
    Buyer-->>Delivery: Confirm receipt
    Delivery-->>Marketplace: Update delivery status
    Marketplace-->>Seller: Complete transaction
    Marketplace-->>Buyer: Complete transaction
```