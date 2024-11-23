import streamlit as st
import pandas as pd
import os

# Đường dẫn file phannhom.csv
OUTPUT_PATH = 'phannhom.csv'

# CSS tùy chỉnh
st.markdown(
    """
    <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    </head>
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
    }
    .web {
        max-width: 800px;
        margin: 0;
        padding: 0;
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

# Kiểm tra sự tồn tại của file phannhom.csv
if not os.path.exists(OUTPUT_PATH):
    st.error("File kết quả không tồn tại. Vui lòng chạy mô hình trước để tạo phannhom.csv!")
else:
    # Đọc dữ liệu từ file phannhom.csv
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
            try:
                filters.append(df["GPA"] == float(gpa))
            except ValueError:
                st.error("GPA phải là số!")
        if so_thich:
            filters.append(df["Sở Thích"] == so_thich)
        if ky_nang:
            filters.append(df["Kỹ Năng"] == ky_nang)

        # Kiểm tra nếu không có điều kiện lọc
        if not filters:
            st.warning("Vui lòng nhập ít nhất một trường thông tin!")
        else:
            try:
                # Áp dụng bộ lọc để tìm kiếm
                result = df
                for condition in filters:
                    result = result.loc[condition]

                if not result.empty:
                    st.success("Kết quả phân nhóm:")

                    # Hiển thị kết quả trong bảng đơn giản
                    st.markdown('<div class="web">', unsafe_allow_html=True)
                    for _, row in result.iterrows():
                        st.markdown(
                            f"""
                            <div style="margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                                <strong>Họ Tên:</strong> {row["Họ Tên"]} <br>
                                <strong>Nhóm:</strong> {row["Nhóm"]}
                            </div>
                            """, unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("Không tìm thấy thông tin phù hợp trong dữ liệu.")
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")










