SELECT students_groups.group_id,
       students_count,
       average_grade,
       students_pass_count,
       students_missed_count,
       students_repeated_count
FROM students_groups
INNER JOIN (
    SELECT assignments.group_id,
           AVG(assignments_grades.grade) AS average_grade,
           SUM(assignments_grades.date > assignments.due_date) AS students_missed_count,
           COUNT(assignments_grades.student_id)
               - COUNT(DISTINCT assignments_grades.student_id) AS students_repeated_count
    FROM assignments
    INNER JOIN assignments_grades
    ON assignments.assisgnment_id = assignments_grades.assisgnment_id
    GROUP BY assignments.group_id
    ) AS table_assignments
ON students_groups.group_id = table_assignments.group_id
INNER JOIN (
    SELECT students.group_id,
           COUNT(DISTINCT students.student_id) as students_count,
           COUNT(DISTINCT students.student_id)
               - COUNT(DISTINCT assignments_grades.student_id) as students_pass_count
    FROM students
    LEFT JOIN assignments_grades
    ON students.student_id = assignments_grades.student_id
    GROUP BY students.group_id
    ) AS table_students
ON students_groups.group_id = table_students.group_id
GROUP BY students_groups.group_id

