SELECT
    Metric,
    SUM(CASE WHEN UPPER(SUBSTRING(last_name, 1, 1)) <= 'H' THEN 1 ELSE 0 END) AS 'Last Name A-H',
    SUM(CASE WHEN UPPER(SUBSTRING(last_name, 1, 1)) > 'H' AND UPPER(SUBSTRING(last_name, 1, 1)) <= 'P' THEN 1 ELSE 0 END) AS 'Last Name I-P',
    SUM(CASE WHEN UPPER(SUBSTRING(last_name, 1, 1)) > 'P' THEN 1 ELSE 0 END) AS 'Last Name Q-Z',
    SUM(CASE WHEN last_name IS NULL THEN 1 ELSE 0 END) AS 'No Last Name'
FROM
    (SELECT 'Members' AS Metric, last_name
     FROM members
     UNION ALL
     SELECT 'Eligibility Checks' AS Metric, last_name
     FROM members, eligibility_checks
     WHERE members.member_id = eligibility_checks.member_id
     UNION ALL
     SELECT 'Enrollments' AS Metric, last_name
     FROM members, enrollments
     WHERE members.member_id = enrollments.member_id)
GROUP BY Metric
ORDER BY
    CASE Metric
        WHEN 'Members' THEN 1
        WHEN 'Eligibility Checks' THEN 2
        WHEN 'Enrollments' THEN 3
    END