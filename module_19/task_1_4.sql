SELECT group_id,
       AVG(overdue_tasks_count) AS average_overdue_tasks_count,
       MAX(overdue_tasks_count) AS max_overdue_tasks_count,
       MIN(overdue_tasks_count) AS min_overdue_tasks_count
FROM (
    SELECT assignments.group_id,
           SUM(assignments_grades.date > assignments.due_date) as overdue_tasks_count
    FROM assignments
    INNER JOIN assignments_grades
    ON assignments.assisgnment_id = assignments_grades.assisgnment_id
    GROUP BY assignments.group_id, assignments.assisgnment_id
    )
GROUP BY group_id