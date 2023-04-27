SELECT "order".order_no, customer.full_name
FROM customer
INNER JOIN "order"
ON customer.customer_id = "order".customer_id
WHERE customer.manager_id IS NULL