SELECT students.full_name
FROM students
WHERE students.group_id = (
    SELECT students_groups.group_id
    FROM students_groups
    WHERE students_groups.teacher_id = (
        SELECT teachers.teacher_id
        FROM teachers
        INNER JOIN assignments
        ON teachers.teacher_id = assignments.teacher_id
        INNER JOIN assignments_grades
        ON assignments.assisgnment_id = assignments_grades.assisgnment_id
        GROUP BY teachers.teacher_id
        ORDER BY AVG(assignments_grades.grade) DESC
        LIMIT 1
         )
     );

SELECT students.full_name
FROM students
INNER JOIN students_groups
ON students.group_id = students_groups.group_id
INNER JOIN (
    SELECT teachers.teacher_id
    FROM teachers
    INNER JOIN assignments
    ON teachers.teacher_id = assignments.teacher_id
    INNER JOIN assignments_grades
    ON assignments.assisgnment_id = assignments_grades.assisgnment_id
    GROUP BY teachers.teacher_id
    ORDER BY AVG(assignments_grades.grade) DESC
    LIMIT 1
    ) AS easy_teacher
ON students_groups.teacher_id = easy_teacher.teacher_id;