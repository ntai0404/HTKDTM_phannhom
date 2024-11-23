import streamlit as st
import pandas as pd
import os

# Đường dẫn file output CSV
OUTPUT_PATH = 'output.csv'

# CSS tùy chỉnh
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
    }
    .web {
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .header {
        text-align: center;
        margin-bottom: 20px;
        background-image: url(https://www.workhuman.com/_next/image/?url=https%3A%2F%2Fimages.ctfassets.net%2Fhff6luki1ys4%2F2xNpvX7DjQC0L8k11uDOOO%2Fcc13cc48ebe85e2a59134597c85420e6%2FGroup-high-five-of-a-diverse-team-of-employees-in-an-office.png&w=3840&q=75);
        background-size: cover; 
        background-position: center;
        padding: 40px 20px; 
        color: #fff;
        border-radius: 8px;
    }
    .header h1 {
        font-size: 44px;
        margin: 0;
        color: #FFFAFA;
    }
    </style>
    """, unsafe_allow_html=True
)

# Tiêu đề ứng dụng
st.markdown('<div class="header"><h1>Phân nhóm các thành viên</h1></div>', unsafe_allow_html=True)

# Kiểm tra sự tồn tại của file output.csv
if not os.path.exists(OUTPUT_PATH):
    st.error("File kết quả không tồn tại. Vui lòng chạy mô hình trước!")
else:
    # Đọc dữ liệu từ file output.csv
    df = pd.read_csv(OUTPUT_PATH)

    # Hiển thị form nhập liệu
    with st.form("input_form"):
        ho_ten = st.text_input("Họ Tên")
        gpa = st.text_input("GPA")
        so_thich = st.text_input("Sở Thích")
        ky_nang = st.text_input("Kỹ Năng")
        submit_button = st.form_submit_button("Tìm nhóm")

    # Xử lý khi nhấn nút "Tìm nhóm"
    if submit_button:
        # Tạo điều kiện lọc động dựa trên các trường không rỗng
        filters = []
        if ho_ten:
            filters.append(df["Họ Tên"] == ho_ten)
        if gpa:
            filters.append(df["GPA"] == float(gpa))
        if so_thich:
            filters.append(df["Sở Thích"] == so_thich)
        if ky_nang:
            filters.append(df["Kỹ Năng"] == ky_nang)

        if filters:
            try:
                # Áp dụng bộ lọc để tìm kiếm
                result = df
                for condition in filters:
                    result = result.loc[condition]

                if not result.empty:
                    st.success("Kết quả tìm kiếm:")
                    st.dataframe(result[["Họ Tên", "Nhóm"]])
                else:
                    st.warning("Không tìm thấy thông tin phù hợp trong dữ liệu.")
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")
        else:
            st.warning("Vui lòng nhập ít nhất một trường thông tin!")


