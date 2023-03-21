# match flowsheet on the event's inpatient_id and the patient ID
# filter to 1 hour prior to admit
# saved results as traige_TE.draft_cohort_flowsheet_1hr_prior_to_admit
select * from
  (select * 
    from traige_TE.draft_cohort_inpatient_id as cohort
    left join 
      (select rit_uid, inpatient_data_id_coded as inpat_coded, template, 
              row_disp_name, recorded_time_jittered_utc, num_value1, num_value2,
        from traige_TE.flowsheet_draft_cohort_select_row_display_names
      )
    on cohort.inpatient_data_id_coded = inpat_coded
    and cohort.jc_uid = rit_uid
  )
where timestamp_add(recorded_time_jittered_utc, INTERVAL 1 HOUR) <= admit_time_jittered