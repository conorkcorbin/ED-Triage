# filter labs to include only those prior to 1 hr of admit
# stored results as traige_TE.draft_cohort_labs_1hr_prior_to_admit
select * 
  from traige_TE.draft_cohort_joined_labs_uid_csn
  where timestamp_add(order_time_jittered_utc, INTERVAL 1 HOUR) <= admit_time_jittered