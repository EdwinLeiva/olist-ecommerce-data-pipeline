# Olist E-commerce Database Schema

## 1. Overview

The Olist e-commerce database is designed to store and analyze information about customers, orders, products, product categories, and order items.

The database uses PostgreSQL and follows a relational structure with primary keys, foreign keys, constraints, and indexes to maintain data integrity and improve query performance.

## 2. Database Tables

### 2.1 customers

Stores customer information.

| Column | Description |
|---|---|
| customer_id (PK) | Unique customer identifier |
| customer_unique_id | Customer's unique identifier |
| customer_zip_code_prefix | Brazilian postal code prefix |
| customer_city | Customer's city |
| customer_state | Brazilian state code |

### 2.2 orders

Stores order information and timestamps.

| Column | Description |
|---|---|
| order_id (PK) | Unique order identifier |
| customer_id (FK) | References customers |
| order_status | Current order status |
| order_purchase_timestamp | Purchase timestamp |
| order_approved_at | Approval timestamp |
| order_delivered_carrier_date | Carrier delivery timestamp |
| order_delivered_customer_date | Customer delivery timestamp |
| order_estimated_delivery_date | Estimated delivery date |

### 2.3 order_items

Stores individual products included in each order.

| Column | Description |
|---|---|
| order_id (PK, FK) | References orders |
| order_item_id (PK) | Item sequence within an order |
| product_id (FK) | References products |
| seller_id | Seller identifier |
| shipping_limit_date | Shipping deadline |
| price | Product price |
| freight_value | Shipping cost |

**Primary key:** Composite key (`order_id`, `order_item_id`).

### 2.4 products

Stores product attributes.

| Column | Description |
|---|---|
| product_id (PK) | Unique product identifier |
| product_category_name (FK) | References product_categories; nullable |
| product_name_lenght | Product name length |
| product_description_lenght | Product description length |
| product_photos_qty | Number of product photos |
| product_weight_g | Product weight in grams |
| product_length_cm | Product length in centimeters |
| product_height_cm | Product height in centimeters |
| product_width_cm | Product width in centimeters |

### 2.5 product_categories

Stores unique product category names.

| Column | Description |
|---|---|
| product_category_name (PK) | Unique product category name |

## 3. Relationships

| Parent Table | Child Table | Relationship |
|---|---|---|
| customers | orders | One-to-many |
| orders | order_items | One-to-many |
| products | order_items | One-to-many |
| product_categories | products | One-to-many |

## 4. Primary Keys

- `customers`: `customer_id`
- `orders`: `order_id`
- `order_items`: (`order_id`, `order_item_id`)
- `products`: `product_id`
- `product_categories`: `product_category_name`

## 5. Foreign Keys

| Foreign Key | Referenced Key |
|---|---|
| orders.customer_id | customers.customer_id |
| order_items.order_id | orders.order_id |
| order_items.product_id | products.product_id |
| products.product_category_name | product_categories.product_category_name |

## 6. Indexes

PostgreSQL automatically creates unique indexes for primary keys.

Additional indexes created to support joins and filtering:

| Index | Table | Column |
|---|---|---|
| idx_orders_customer_id | orders | customer_id |
| idx_order_items_product_id | order_items | product_id |
| idx_products_category_name | products | product_category_name |

The composite primary key index on `order_items` also supports lookups using `order_id` as its leading column.

## 7. Data Integrity

The database implements:

- Primary key constraints to ensure unique records.
- Foreign key constraints to maintain referential integrity.
- NOT NULL constraints for required fields.
- CHECK constraints to validate order statuses and Brazilian state codes.
- Nullable product categories to accommodate products without a category.

## 8. Data Quality Validation

The four foreign key relationships were validated using LEFT JOIN queries.

**Validation result:** Zero orphan records across all four relationships.

The database contains 610 products without an assigned category. These records are intentionally allowed because `products.product_category_name` is nullable.

## 9. Design Considerations

- Product categories are stored separately to reduce repeated category values.
- Numeric product attributes use integer types where appropriate.
- Monetary values in `order_items` use `NUMERIC(10,2)` for decimal precision.
- Additional indexes support frequently used joins and filtering operations.
- The database structure supports incremental, idempotent data loading through the ETL pipeline.

---

**Project:** Olist E-commerce Data Pipeline  
**Database:** PostgreSQL  
**Schema:** public