select s.id s_id
			, s.full_name s_name
			, s2.subject_name subject_name
			, avg(m.mark) as avg_mark
		from hw6.students s
		inner join hw6.marks m on s.id = m.student_id
		inner join hw6.subjects s2 on s2.id = m.subject_id
		group by s.id, s.full_name, s2.subject_name
		having s2.subject_name = 'set subject here'
		order by s2.subject_name, avg(m.mark) desc
		fetch first 1 rows only