# Web-Scraper

## Overview
Scraping websites based on the URLs from Excel, Text or User Input
The URLs should be stored in a Excel file in **.xlsx** format, or in a **.txt** format as a Text Document or can manually write the URLs

## Required Softwares
1. Python
2. SQL

## Required Modules
1. requests
2. beautifulsoup4
3. lxml
4. mysql-connector-python
5. pandas
6. openpyxl

## Steps for Setting up MySQL
1. Download the installer from this [here](https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-documents-8.0.38.msi). You need to have an Oracle Account for this.
2. Then open the installer and you will have a Licence Agrrement, click on Agree and then you will have window like,

   ![image](https://github.com/Shashank-okrms/Web-Scraper/assets/96413845/3c96dd40-80fe-4360-a5a0-0c126adb019e)

    Click on the **Full** option, then choose the installation location and then keep on clicking **Next** option
3. Then at the **Installation** tab, click on **Execute**. Wait for some time and then click on **Next** button
4. Then at **Account and Roles** tab, choose a Root Password for your server and remember it. Then click on **Next** and then **Execute** button then the **Finish** button
5. Then give the required deatils for the server to run. MySQL will now be setup

If you are stuck anywhere, refer this for the full process [video](https://www.youtube.com/watch?v=GIRcpjg-3Eg)

## Steps for Running the Code
1. Primarily, check whether all the **Required Modules** are installed by using the following pip command, **pip 'modlue_name' --version**
2. Clone this repo or downlaod the file slocally and open it with your installed Code Editor like VSCode, PyCharm, Spyder etc.,
3. The repo will have **web_scraper.py** file which is the main file, along with that **db-setup.sql** is a setup file for the SQL database, which will have the name of the database and the table name and the columns it is supposed to have with its datatype.
4. In the **web_scraper.py** file, it is importtant to change the **password** in db_config which will be in the start of the program. if you change the databse nam ein **db_setup.sql** file, you have to change the name of the **database** in db_config part.

    ![Screenshot (82)](https://github.com/Shashank-okrms/Web-Scraper/assets/96413845/3cda08d1-1c9a-482f-a1b6-5b3606adeb87)

5. Then, click on the **RUN** button for the code to run and the select the option whether you want the input to be given as a Excel file, Text file or by the User input,

    ![Screenshot (83)](https://github.com/Shashank-okrms/Web-Scraper/assets/96413845/e3f19e68-f988-4a12-9620-97c52383af3b)

6. Then you can have the .csv file which have all the fields mentioned in the **db_setup.sql** file and you can even check mysql, you can follow the below steps to check the data
   - USE 'Database_Name';
   - SHOW TABLES;
   - SELECT * FROM 'Table_Name';
7. To empty the table you can use **TRUNCATE TABLE 'Table_Name';**. This will empty the table without deleting the columns but removes only the values.
