# join conor's cohort with inpatient id for labs
# stored as traige_TE.draft_cohort_inpatient_id
select cohort.jc_uid, cohort.pat_enc_csn_id_coded, inpatient_data_id_coded, admit_time_jittered, label 
  from conor_db.triage_cohort_draft as cohort
  left join (select jc_uid, pat_enc_csn_id_coded, inpatient_data_id_coded
             from starr_datalake2018.encounter
             ) as enc
  on cohort.jc_uid = enc.jc_uid
    and cohort.pat_enc_csn_id_coded = enc.pat_enc_csn_id_coded