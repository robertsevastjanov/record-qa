SELECT count(*) FROM cases;

SELECT status, count(*) FROM cases GROUP BY status;

SELECT case_id, count(*)
FROM cases
GROUP BY case_id
HAVING count(*) > 1;
