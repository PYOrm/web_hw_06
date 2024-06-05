select g.group_name,
		s.full_name
	from hw6.students s
	inner join hw6."groups" g on g.id = s.group_id
	where g.group_name = 'set group name here'