select s.id
	, s.full_name
	, avg(m.mark) as avg_mark
from hw6.students s
inner join hw6.marks m on s.id = m.student_id
group by s.id, s.full_name
order by avg(m.mark) desc
fetch first 5 rows only