SELECT AVG(overdue_tasks_count) as average_overdue_tasks_count,
       MAX(overdue_tasks_count) as max_overdue_tasks_count,
       MIN(overdue_tasks_count) as min_overdue_tasks_count
FROM (
    SELECT SUM(assignments_grades.date > assignments.due_date) as overdue_tasks_count
    FROM assignments
    INNER JOIN assignments_grades
    ON assignments.assisgnment_id = assignments_grades.assisgnment_id
    GROUP BY assignments.group_id
    );

