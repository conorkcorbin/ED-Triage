/* right join doesn't work here because the where clause is after join
for right join to work, do the where filter before joining
*/
SELECT c.anon_id, c.pat_enc_csn_id_coded, c.admit_time_jittered,
    o.order_type, o.order_status, o.display_name, o.description, 
    o.order_time_jittered_utc
FROM 
    `som-nero-phi-jonc101.shc_core.order_proc` as o
RIGHT JOIN 
    `som-nero-phi-jonc101.triage.triage_cohort_draft_2019` as c
ON (c.anon_id=o.anon_id and c.pat_enc_csn_id_coded=o.pat_enc_csn_id_coded)
WHERE 
    o.order_type = "Admission"
AND
    (
    UPPER(o.display_name) LIKE UPPER('%Admit to Inpatient%')
    OR o.description = "ADMIT TO INPATIENT"
    )

ORDER BY
  c.anon_id