# Task_2 #

## Question 1 ##

Вопрос:

    Телефоны какого цвета чаще всего покупают?

Ответ:

    Violet

Был выполнен следующий код:

```SQL
SELECT phone_color, MAX(sold_count) 
FROM table_checkout;
```

Результат:

![Result 1][1]
***


## Question 2 ##

Вопрос:

    Какие телефоны чаще покупают: красные или синие?

Ответ:

    Red

Был выполнен следующий код:

```SQL
SELECT phone_color, sold_count 
FROM table_checkout 
WHERE phone_color IN ('Blue', 'Red');
```

Результат:

![Result 2][2]
***


## Question 3 ##

Вопрос:

    Какой самый непопулярный цвет телефона?

Ответ:

    Goldenrod

Был выполнен следующий код:

```SQL
SELECT phone_color, MIN(sold_count)
FROM table_checkout;
```

Результат:

![Result 3][3]
***
    
[1]: ./result_1.jpg "Result 1"
[2]: ./result_2.jpg "Result 2"
[3]: ./result_3.jpg "Result 3"

