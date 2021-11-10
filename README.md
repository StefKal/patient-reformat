# patient-reformat
This is a script that reformats the patient data for Dr. Stefanidou Kyriaki M.D. 

The program takes in an excel file and using pandas, xlsxwriter, and regex reformats the file based on the client's needs. 
The main problem was that tha patient data was irrelular and not consistent. 
The input was an excel sheet that consisted of columns with patient names, and patient prescription followed by dates. 
The main issues were two:
  -the patient prescription were not always separated in different columns 
  -the dates were in irregular formats such as (x.x.xxx, x/x/xxxx/) and sometimes mistakenly written like (1..2.2021)

The program works in a way so we can split everything down in order to strip the data of mistakes and re-format the data in the correct way
The output file will return an excel file with columns ['Last Name', 'First Name', 'Date', 'Prescription'])
