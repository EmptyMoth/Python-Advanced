SELECT students.full_name
FROM students
INNER JOIN assignments_grades
ON students.student_id = assignments_grades.student_id
GROUP BY students.student_id
ORDER BY AVG(assignments_grades.grade) DESC
LIMIT 10