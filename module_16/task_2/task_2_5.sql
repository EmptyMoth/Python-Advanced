SELECT customer_1.full_name, customer_2.full_name
FROM customer as customer_1
INNER JOIN customer as customer_2
ON customer_1.city = customer_2.city
       AND customer_1.manager_id = customer_2.manager_id
       AND customer_1.full_name != customer_2.full_name
