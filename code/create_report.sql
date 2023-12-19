select substring(Metric,3,length(Metric)-2) as Metric,
       sum(last_name_a_h) as 'Last Name A-H',
       sum(last_name_i_p) as 'Last Name I-P',
       sum(last_name_q_z) as 'Last Name Q-Z',
       sum(no_last_name) as 'No Last Name'
from
    (select Metric,
           case
                when upper(SUBSTRING(last_name, 1, 1)) <= 'H' THEN 1
                else 0
            end as last_name_a_h,
            case
                when upper(SUBSTRING(last_name, 1, 1)) > 'H' and upper(SUBSTRING(last_name, 1, 1)) <= 'P' THEN 1
                else 0
            end as last_name_i_p,
            case
                when upper(SUBSTRING(last_name, 1, 1)) > 'P' then 1
                else 0
            end as last_name_q_z,
            case
                when last_name is null then 1
                else 0
            end as no_last_name,
            member_id
    from
        (select '1:Members' as Metric, last_name, member_id
         from members
         union
         select '2:Eligibility Checks' as Metric, last_name, eligibility_checks.member_id
         from members, eligibility_checks where members.member_id = eligibility_checks.member_id
         union
         select '3:Enrollments' as Metric, last_name, enrollments.member_id
         from members, enrollments where members.member_id = enrollments.member_id))
group by Metric
