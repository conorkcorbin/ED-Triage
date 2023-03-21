# flowsheet - filter to select row_disp_name and cohort draft patients - 46,957,162
# saved as flowsheet_draft_cohort
select rit_uid, inpatient_data_id_coded, template, 
       row_disp_name, recorded_time_jittered_utc, num_value1, num_value2,
from starr_datalake2018.flowsheet
where rit_uid in
  (select jc_uid from conor_db.triage_cohort_draft)
and
(
(row_disp_name="BP")
OR
(row_disp_name="NIBP")
OR
(row_disp_name="Resting BP")
OR
(row_disp_name="Pulse")
OR
(row_disp_name="Heart Rate")
OR
(row_disp_name="Resting HR")
OR
(row_disp_name="Weight")
OR
(row_disp_name="Height")
OR
(row_disp_name="Temp")
OR
(row_disp_name="Resp")
OR
(row_disp_name="Resp Rate")
OR
(row_disp_name="Resting RR")
OR
(row_disp_name="SpO2")
OR
(row_disp_name="Resting SpO2")
OR
(row_disp_name="O2 (LPM) Arterial Systolic BP")
OR
(row_disp_name="Arterial Diastolic BP")
OR
(row_disp_name="Temp (in Celsius)")
OR
(row_disp_name="Blood Pressure")
OR
(row_disp_name="Oxygen Saturation")
OR
(row_disp_name="Glasgow Coma Scale Score")
OR
(row_disp_name="Altered Mental Status (GCS<15)")
OR
(row_disp_name="Total GCS Points")
OR
(row_disp_name="GCS Score")
)