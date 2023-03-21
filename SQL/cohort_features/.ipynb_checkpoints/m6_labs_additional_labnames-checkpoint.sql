# output: traige_cohort_2019_labs_basename_filtered
select * 
from triage.triage_cohort_2019_all_labs as labs
where labs.lab_name in 
("Basophils, ABS (man diff)", "Baso, ABS (man diff)", "Eosinophils, ABS (man diff)", "Eos, ABS (man diff)", "Lymphocytes, ABS (man diff)", "Lym, ABS (man diff)", "Lymphocytes, Abs.", "Monocytes, ABS (man diff)", "Mono, ABS (man diff)", "Neut, ABS (man diff)", "Neut, ABS (Seg+Band) (man diff)", "Neutrophils, Absolute (Manual Diff)", "Glucose, Non-fasting", "Glucose", "Base Excess Arterial for POC", "Bicarbonate, Art for POC", "Hct (Est)", "HCT, POC", "Hematocrit (Manual Entry) See EMR for details", "Hgb, calculated, POC", "HgB", "Potassium, whole blood, ePOC", "Potassium", "Lactic Acid", "Oxygen Saturation for POC", "Arterial pCO2 for POC", "pH by Meter", "Arterial pH for POC", "Platelets", "Arterial pO2 for POC", "Total Bilirubin", "TCO2, (ISTAT)", "CO2 Arterial Total for POC", "Troponin I, POCT", "WBC count")
and labs.pat_enc_csn_id_coded in
(select distinct(cohort.pat_enc_csn_id_coded) from triage.triage_cohort_final as cohort)
