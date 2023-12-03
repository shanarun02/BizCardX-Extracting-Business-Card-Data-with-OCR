import mysql.connector
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re
from io import BytesIO

reader = easyocr.Reader(['en'])
conn=mysql.connector.connect (host='localhost',
                              user='root',
                              password='Arun@5851',
                              database='youtube')
cursor=conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS business_card_datas
                   (company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number TEXT,
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code TEXT,
                    image BLOB
                    )''')
#Side bar creation :
selected = st.sidebar.selectbox("Select Option to Work", ["Upload", "Show"])
if selected == "Upload":
    st.markdown("### Upload a Business Card")
    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:

        def save_card(uploaded_card):
            with open(os.path.join("uploaded_cards", uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())
        save_card(uploaded_card)
        def image_preview(image, res):
            for (bbox, text, prob) in res:
                # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15, 15)
            plt.axis('off')
            plt.imshow(image)
        # DISPLAYING THE UPLOADED CARD
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)
        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Processing image Please wait ..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))
        #easy OCR
        saved_img = os.getcwd()+ "\\" + "uploaded_cards"+ "\\"+ uploaded_card.name
        result = reader.readtext(saved_img,detail = 0,paragraph=False)

        def binary_img(file_path):
            with open(file_path, 'rb') as file:
                binaryData = file.read()
            return binaryData
        data = {"company_name": [],
                "card_holder": [],
                "designation": [],
                "mobile_number": [],
                "email": [],
                "website": [],
                "area": [],
                "city": [],
                "state": [],
                "pin_code": [],
                "image": binary_img(saved_img)
                }

        def get_data(res):
            for ind, i in enumerate(res):
                if "www " in i.lower() or "www." in i.lower():  # Website with 'www'
                    data["website"].append(i)
                elif "WWW" in i:  # In case the website is in the next elements of the 'res' list
                    website = res[ind + 1] + "." + res[ind + 2]
                    data["website"].append(website)
                elif '@' in i:
                    data["email"].append(i)
                # To get MOBILE NUMBER
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) == 2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])
                # To get COMPANY NAME
                elif ind == len(res) - 1:
                    data["company_name"].append(i)
                # To get Card Holder Name
                elif ind == 0:
                    data["card_holder"].append(i)
                #To get designation
                elif ind == 1:
                    data["designation"].append(i)

                #To get area
                if re.findall('^[0-9].+, [a-zA-Z]',i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-z]+',i):
                    data["area"].append(i)
                #To get city name
                match1 = re.findall('.+St , ([a-zA-Z]+).+',i)
                match2 = re.findall('.+St,,([a-zA-Z]+).+',i)
                match3 = re.findall('^[E].*',i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])

                #To get state name
                state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                if state_match:
                    data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                    data["state"].append(i.split()[-1])
                if len(data["state"]) == 2:
                    data["state"].pop(0)

                #To get Pincode
                if len(i) >= 6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    data["pin_code"].append(i[10:])
        get_data(result)

        #Creating a dataframe and storing in DB
        def create_df(data):
            df = pd.DataFrame(data)
            return df
        df = create_df(data)
        st.success("### Data Extracted ")
        st.dataframe(df)
        enable_edit = st.checkbox("Edit data before upload")
        if enable_edit:
           company_name = st.text_input("Company Name", df["company_name"].iloc[0]) 
           card_holder = st.text_input("Card Holder", df["card_holder"].iloc[0])
           designation = st.text_input("Designation", df["designation"].iloc[0])
           mobile_number = st.text_input("mobile_number", df["mobile_number"].iloc[0]) 
           email = st.text_input("email", df["email"].iloc[0]) 
           website = st.text_input("website", df["website"].iloc[0]) 
           area = st.text_input("area", df["area"].iloc[0])
           city = st.text_input("city", df["city"].iloc[0])
           state = st.text_input("state", df["state"].iloc[0]) 
           pin_code = st.text_input("pin_code", df["pin_code"].iloc[0])
           image = st.text_input("image", df["image"].iloc[0])
           # And so on for every column
        
           updated_data = {
              "company_name": company_name,
              "card_holder": card_holder,
              "designation": designation,
              "mobile_number": mobile_number,
              "email": email,
              "website": website,
              "area": area,
              "city": city,
              "state": state,
              "pin_code": pin_code,
              "image": binary_img(saved_img)  # Update this line
          }
            
           updated_df = pd.DataFrame(updated_data, index=[0])
           st.dataframe(updated_df)
           if st.button("Upload to Database"):
               for i, row in updated_df.iterrows():
                   placeholders = ', '.join(['%s' for _ in range(len(row))])
                   columns = ', '.join(updated_df.columns)
                   sql = f"INSERT INTO business_card_datas ({columns}) VALUES ({placeholders})"
                   cursor.execute(sql, tuple(row))
                   conn.commit()
               st.success("Uploaded to the database successfully ")

   

if selected == "Show":
    st.title("Business Card Records")

    # Select all records from the database
    sql = "SELECT * FROM business_card_datas"
    cursor.execute(sql)
    records = cursor.fetchall()
    if not records:
        st.warning("No records found in the database.")
    else:
        # Display records in a DataFrame
        columns = [desc[0] for desc in cursor.description]
        records_df = pd.DataFrame(records, columns=columns)
        st.dataframe(records_df)

        # Multiselect to choose records to display
        selected_records = st.multiselect("Select records to display", records_df.index)

        # Display image for selected records
        for index in selected_records:
            binary_data = records_df.loc[index, "image"]  # Assuming that the image is stored in the "image" column
            if binary_data:
                # Convert binary data to BytesIO
                image_stream = BytesIO(binary_data)

                # Open image using PIL (Python Imaging Library)
                image = Image.open(image_stream)

                # Display image in Streamlit
                st.image(image, caption=f'Business Card Image - Record {index}', use_column_width=True)

# Close the database connection when done
conn.close()

