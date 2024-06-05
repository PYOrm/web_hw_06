select g.group_name,
		s2.subject_name,
		s.full_name,
		m.mark
	from hw6.marks m
	inner join hw6.subjects s2 on s2.id = m.subject_id
	inner join hw6.students s on s.id = m.student_id
	inner join hw6."groups" g on g.id = s.group_id
	where g.group_name = 'group_1' and s2.subject_name ='History'