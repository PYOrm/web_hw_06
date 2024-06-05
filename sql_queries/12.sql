with subjname (subj, grp) as (values ('set subject here', 'set group name here'))
select  s.full_name,
		m.mark,
		m."timestamp"::date
from hw6.marks m,
	 hw6.students s,
	 hw6.subjects s2,
	 hw6."groups" g,
	 subjname,
	 (select max(m."timestamp"::date) lastdate
		from hw6.marks m,
		hw6.subjects s,
		hw6."groups" g,
		hw6.students s3,
		subjname
		where m.subject_id = s.id
		and g.id = s3.group_id
		and m.student_id = s3.id
		and s.subject_name = subj
		and g.group_name = grp) ts
where g.group_name = grp
	and s2.subject_name = subj
	and m.student_id = s.id
	and m.subject_id = s2.id
	and m."timestamp"::date = ts.lastdate
	and s.group_id = g.id
order by  m."timestamp"::date desc