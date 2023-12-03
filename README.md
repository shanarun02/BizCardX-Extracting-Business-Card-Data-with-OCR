# BizCardX-Extracting-Business-Card-Data-with-OCR
Problem Statement :
You have been tasked with developing a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information should include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code. The extracted information should then be displayed in the application's graphical user interface (GUI).
In addition, the application should allow users to save the extracted information into a database along with the uploaded business card image. The database should be able to store multiple entries, each with its own business card image and extracted information.


Approach :
Install the required packages: You will need to install Python, Streamlit, easyOCR, and a database management system like SQLite or MySQL.
Design the user interface: Create a simple and intuitive user interface using Streamlit that guides users through the process of uploading the business card image and extracting its information. You can use widgets like file uploader, buttons, and text boxes to make the interface more interactive.
Implement the image processing and OCR: Use easyOCR to extract the relevant information from the uploaded business card image. You can use image processing techniques like resizing, cropping, and thresholding to enhance the image quality before passing it to the OCR engine.
Display the extracted information: Once the information has been extracted, display it in a clean and organized manner in the Streamlit GUI. You can use widgets like tables, text boxes, and labels to present the information.
Implement database integration: Use a database management system like SQLite or MySQL to store the extracted information along with the uploaded business card image. You can use SQL queries to create tables, insert data, and retrieve data from the database, Update the data and Allow the user to delete the data through the streamlit UI.
Test the application: Test the application thoroughly to ensure that it works as expected. You can run the application on your local machine by running the command streamlit run app.py in the terminal, where app.py is the name of your Streamlit application file.
Improve the application: Continuously improve the application by adding new features, optimizing the code, and fixing bugs. You can also add user authentication and authorization to make the application more secure.
