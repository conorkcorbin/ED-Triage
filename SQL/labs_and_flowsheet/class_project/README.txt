This folder contains the SQL queries used in BigQuery to get the labs and flowsheet data.

FILES:

---
01_add_inpatient_id_to_cohort.sql

SQL:
Adds the inpatient ID associated with the CSN from the Encounters table to the draft_cohort table. The inpatient ID is needed to connect the Flowsheet table to the event.

OUTPUT:
traige_TE.draft_cohort_inpatient_id


---

02_grab_labs.sql

SQL: 
Queries labs based on matched CSNs and patient ID. Selects a set of specific lab_names that were chosen for their utiltity. Joins these labs to the draft_cohort. NO time filter yet.

OUTPUT:
traige_TE.draft_cohort_joined_labs_uid_csn


---

03.labs_filter_time.sql

SQL:
Filters labs based on their order_time_jittered_utc to include labs ordered 1 hr prior to admit for the draft_cohort.

OUTPUT:
traige_TE.draft_cohort_labs_1_hr_prior_to_admit


---

03.2_labs_filter_adjusted_cohort.sql

SQL:
Joins the labs to the traige_cohort_adjusted table. Uses the traige_TE.draft_cohort_joined_labs_uid_csn for lab data since the adjusted_cohort is a subset of the draft_cohort. Filters the results based on the new admit time that has been adjusted in the adjusted_cohort. Filtering is on order_time for labs at 1 hr prior to admit.

OUTPUT:
traige_TE.triage_cohort_adjusted_labs


---

03.3_labs_adjusted_cohort_resulttime.sql

SQL:
Joins labs to the adjusteed_cohort and filters based on RESULT_TIME rather than on order_time of labs.

OUTPUT:
traige_TE.triage_cohort_adjusted_labs_resulttime


---

04_grab_flowsheet.sql

SQL:
Grabs the Flowsheet data for the draft_cohort based on select row_disp_name. Joins on rit_uid to the draft_cohort. NO filtering yet.

OUTPUT:
traige_TE.flowsheet_draft_cohort


---

05_match_and_filter_flowsheet.sql

SQL:
Matches the flowsheet on the inpatient_data_id_coded (event ID) and the jc_uid (patient ID) for the draft_cohort. Filters based on the recorded_time_jittered_utc for the flowsheet at 1 hr prior to admit.

OUTPUT:
traige_TE.draft_cohort_flowsheet_1hr_prior_to_admit


---

05.2_match_filter_flowsheet_adjusted_cohort.sql

SQL:
Mathces the flowsheet to the adjusted_cohort based on inpatient_data_id_coded and rit_uid. Filters by recorded_time_jittered_utc to 1 hr prior to admit.

OUTPUT:
traige_TE.triage_cohort_adjusted_flowsheet