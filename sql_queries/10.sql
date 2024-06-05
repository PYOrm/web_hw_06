select distinct s2.subject_name from hw6.marks m
inner join hw6.students s on s.id = m.student_id
inner join hw6.subjects s2 on s2.id = m.subject_id
inner join hw6.teachers t on t.id = s2.teacher_id
where s.full_name = 'student name here' and t.full_name ='teacher name here'