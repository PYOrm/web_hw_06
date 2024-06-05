select  g.group_name
		, s2.subject_name
		, avg(m.mark) as avg_mark
	from hw6.students s
	inner join hw6.marks m on s.id = m.student_id
	inner join hw6.subjects s2 on s2.id = m.subject_id
	inner join hw6."groups" g on s.group_id = g.id
	group by g.group_name, s2.subject_name
	having s2.subject_name = 'set subject here'
	order by s2.subject_name, avg(m.mark) desc
