cd "../APLC/APLC_apworld/"
del /s /q *.*
rmdir /s /q "../APLC/APLC_apworld/lethal_company"
cd "C:\Users\tyler\OneDrive\Documents\GitHub\Archipelago"
xcopy "C:\users\tyler\onedrive\documents\github\archipelago\worlds\lethal_company" "..\APLC\APLC_apworld\lethal_company" /E /I
cd "C:\Users\tyler\OneDrive\Documents\GitHub\APLC\APLC_apworld"
tar -a -c -f lethal_company.zip lethal_company
ren lethal_company.zip lethal_company.apworld
cd "C:\Users\tyler\OneDrive\Documents\GitHub\Archipelago"
"C:\Users\tyler\OneDrive\Documents\GitHub\Archipelago\Venv\Scripts\python.exe" gen_template_options.py
ren "C:\Users\tyler\OneDrive\Documents\GitHub\Archipelago\Players\Templates\Lethal Company.yaml" "lethal_company.yaml"
move "C:\Users\tyler\OneDrive\Documents\GitHub\Archipelago\Players\Templates\lethal_company.yaml" "C:\Users\tyler\OneDrive\Documents\GitHub\APLC\APLC_apworld"