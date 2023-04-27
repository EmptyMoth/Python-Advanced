SELECT customer.customer_id
FROM customer
WHERE customer.customer_id NOT IN (
    SELECT "order".customer_id
    FROM "order"
    )