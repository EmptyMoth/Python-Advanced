SELECT assignments_grades.assisgnment_id,
       AVG(assignments_grades.grade) as avg_grade
FROM assignments_grades
WHERE assignments_grades.assisgnment_id IN (
    SELECT assignments.assisgnment_id
    FROM assignments
    WHERE assignments.assignment_text LIKE 'прочитать%'
      OR assignments.assignment_text LIKE 'выучить%'
    )
GROUP BY assignments_grades.assisgnment_id