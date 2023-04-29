SELECT teachers.full_name
FROM teachers
INNER JOIN assignments
ON teachers.teacher_id = assignments.teacher_id
INNER JOIN assignments_grades
ON assignments.assisgnment_id = assignments_grades.assisgnment_id
GROUP BY teachers.teacher_id
ORDER BY AVG(assignments_grades.grade)
LIMIT 1