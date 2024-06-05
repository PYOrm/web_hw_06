select s.id,
		s.subject_name
	from hw6.subjects s
	inner join hw6.teachers t on t.id = s.teacher_id
	where t.full_name = 'set name here'