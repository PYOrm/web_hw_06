select t.full_name, avg(m.mark) avg_mark
from hw6.marks m
inner join hw6.subjects s on m.subject_id = s.id
inner join hw6.teachers t on s.teacher_id = t.id
where t.full_name = 'set name here'
group by t.full_name