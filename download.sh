# 1. Go to https://www.dhs.wisconsin.gov/covid-19/vaccine-data.htm
# 2. Under "Vaccine Distribution Summary" section, click "Download"
# 3. Hit "cross tab"
# 4. Hover over each option until you see the one called "Vax Summary - adm spk", check it
# 5. Select CSV for the format
# 6. Click Download
# 7. Click Download again, or copy the link into the curl command below.
curl https://bi.wisconsin.gov/vizql/t/DHS/w/VaccineVisualization-distributionsummary/v/_VaxSummaryall-ship-del-adm/tempfile/sessions/68A3A0D03FF741EC9497A4D18615B66E-4:5/\?key\=2121495922\&keepfile\=yes\&attachment\=yes > vax.csv
