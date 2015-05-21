# phycian_data_stat
To RUN the script for all 3 platforms and 2 years for the required specialty-
./shell.sh

The script calls python script for all the cdv files separately.
USAGE: python ex.py specialty year platform
Input files needed:
crosswalk.txt
state.txt
year/platform/csv/specialty.csv
Outputfiles

results/year/platform/csv/specialty.csv
results/year-platform.csv

results/year-platform-specialty-FFM.txt
results/year-platform-specialty-PM.txt
results/year-platform-specialty-SBM.txt
results/year-platform-specialty-YES.txt
results/year-platform-specialty-NO.txt


results/year-platform-aggregate-FFM.txt
results/year-platform-aggregate-PM.txt
results/2year-platform-aggregate-SBM.txt
results/year-platform-aggregate-YES.txt
results/year-platform-aggregate-NO.txt



EXAMPLE:
python ex.py family_medicine 2013 NEJM

Input files needed: 
crosswalk.txt
state.txt
2013/NEJM/csv/family_medicine.csv

Outputfiles

results/2013/NEJM/csv/family_medicine.csv
results/2013-NEJM.csv

results/2013-NEJM-family_medicine-FFM.txt
results/2013-NEJM-family_medicine-PM.txt
results/2013-NEJM-family_medicine-SBM.txt
results/2013-NEJM-family_medicine-YES.txt
results/2013-NEJM-family_medicine-NO.txt


results/2013-NEJM-aggregate-FFM.txt
results/2013-NEJM-aggregate-PM.txt
results/2013-NEJM-aggregate-SBM.txt
results/2013-NEJM-aggregate-YES.txt
results/2013-NEJM-aggregate-NO.txt
