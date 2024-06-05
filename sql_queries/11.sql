select avg(m.mark)
from hw6.marks m,
	 hw6.students s,
	 hw6.teachers t,
	 hw6.subjects s2
where s.full_name = 'student name here'
	and t.full_name ='teacher name here'
	and m.student_id = s.id
	and m.subject_id = s2.id
	and t.id = s2.teacher_id