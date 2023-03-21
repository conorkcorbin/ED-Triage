select labs.anon_id, labs.pat_enc_csn_id_coded, order_id_coded, lab_name,
      base_name, ord_num_value, reference_low, reference_high, 
      reference_unit, result_in_range_yn, result_flag, 
      result_time_utc, order_time_utc , taken_time_utc,
from shc_core.lab_result as labs
right join traige_TE.triage_cohort_final as cohort # join labs to cohort
on labs.pat_enc_csn_id_coded = cohort.pat_enc_csn_id_coded
and labs.anon_id = cohort.anon_id
where admit_time >= result_time_utc # only labs before admit time
and extract(year from admit_time) > 2014 # only CSNs after 2014

