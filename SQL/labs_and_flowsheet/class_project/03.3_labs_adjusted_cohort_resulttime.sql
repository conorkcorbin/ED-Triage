# Filters the labs based on *result_time* rather than order_time
# for the adjusted_cohort
# stored as traige_TE.triage_cohort_adjusted_labs_resulttime
select newc.jc_uid, newc.pat_enc_csn_id_coded, 
        oldc.order_id_coded, lab_name, ord_value, ord_num_value, 
        reference_low, reference_high, reference_unit, result_in_range_yn,
        result_flag, newc.admit_time, result_time_jittered_utc, order_time_jittered_utc, taken_time_jittered_utc, newc.label,
  from traige_TE.triage_cohort_adjusted as newc
  left join traige_TE.draft_cohort_joined_labs_uid_csn as oldc
  on newc.jc_uid = oldc.jc_uid
  and newc.pat_enc_csn_id_coded = oldc.pat_enc_csn_id_coded
  where timestamp_add(result_time_jittered_utc, INTERVAL 1 HOUR) <= admit_time