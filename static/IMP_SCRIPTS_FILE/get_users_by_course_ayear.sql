
for a.y 2022-23 --- 2
for a.y 2023-24 --- 3
for course MCA --- 2
for course MBA --- 1



select ad.course_id,c.course_name,ad.ay_year_id,acy.ayear, ad.user_id,up.first_name,up.last_name from user_profiles up
left join  iims_tbl_user_academic_details ad on up.user_id=ad.user_id
left join auth_user au on au.id=up.user_id
left join iims_tbl_academic_year acy on acy.id=ad.ay_year_id
left join iims_tbl_course c on ad.course_id=c.id
where ad.ay_year_id =3 and au.is_active=1 and ad.course_id=1