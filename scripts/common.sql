select u.id, u.* from "user" u order by id DESC

TRUNCATE TABLE public.user;

SELECT * FROM "user" order by id LIMIT 100 OFFSET 0

select COUNT(distinct name) from "user"

select COUNT(distinct sur_name) from "user"

select count(8) from "user" u


CREATE INDEX user_name_idx ON public."user" ("name");
drop index user_name_idx;

CREATE INDEX user_sur_name_idx ON public."user" ("sur_name");
drop index user_sur_name_idx;

CREATE INDEX user_sur_name_name_idx ON public."user" ("name", "sur_name");
CREATE INDEX user_sur_name_name_idx ON public."user" ("name" text_pattern_ops, "sur_name" text_pattern_ops);
CREATE INDEX user_sur_name_name_idx ON public."user" (lower("name") text_pattern_ops, lower("sur_name") text_pattern_ops);
drop index user_sur_name_name_idx;

analyze

explain analyze
select * from public.user
where "name" ilike 'Авгу%' and sur_name ilike 'Абра%';

explain analyze
select * from public.user
-- where "name" like lower('Авгу%') and sur_name like lower('Абра%');
where "name" like lower('%Авгу%') and sur_name like lower('%Абра%'); -- работает медленно

explain analyze
select * from public.user
where "name" like 'Авгу%';


select * from public.user
where "name" ilike 'Авгу%' and sur_name ilike 'Абра%';