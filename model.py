import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np

# Đọc dữ liệu từ file CSV
file_path = 'data.csv'  # Đường dẫn tới file CSV
df = pd.read_csv(file_path)

# Tiền xử lý dữ liệu
# Mã hóa cột danh mục (Sở Thích và Kỹ Năng)
encoder = LabelEncoder()
df["Sở Thích"] = encoder.fit_transform(df["Sở Thích"])
df["Kỹ Năng"] = encoder.fit_transform(df["Kỹ Năng"])

# Chuẩn hóa dữ liệu số (GPA, Sở Thích, Kỹ Năng)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[["GPA", "Sở Thích", "Kỹ Năng"]])

# Áp dụng K-Means Clustering (4 cụm)
kmeans = KMeans(n_clusters=4, random_state=42)
df["Nhóm"] = kmeans.fit_predict(scaled_features)

# Chuyển đánh số nhóm từ 0-3 thành 1-4
df["Nhóm"] = df["Nhóm"] + 1

# Điều chỉnh số lượng mỗi nhóm để đảm bảo từ 4 đến 5 người
while True:
    group_sizes = df["Nhóm"].value_counts()
    if all(4 <= count <= 5 for count in group_sizes):
        break  # Nếu đã hợp lệ, thoát vòng lặp
    else:
        # Nhóm có nhiều hơn 5 người, di chuyển người thừa sang nhóm thiếu
        largest_group = group_sizes.idxmax()  # Nhóm có nhiều người nhất
        smallest_group = group_sizes.idxmin()  # Nhóm có ít người nhất

        # Chuyển một người từ nhóm lớn nhất sang nhóm nhỏ nhất
        idx_to_move = df[df["Nhóm"] == largest_group].index[0]
        df.at[idx_to_move, "Nhóm"] = smallest_group

# Kết quả phân cụm
output_file = './output.csv'
df[["Họ Tên", "GPA", "Sở Thích", "Kỹ Năng", "Nhóm"]].to_csv(output_file, index=False)

print(f"\nKết quả đã được lưu vào {output_file}")

# Đọc lại dữ liệu gốc từ data.csv và kết quả phân cụm từ output.csv
df_original = pd.read_csv(file_path)
df_clustered = pd.read_csv(output_file)

# Ghép cột "Nhóm" từ df_clustered vào df_original
df_original["Nhóm"] = df_clustered["Nhóm"]

# Lưu kết quả ghép vào phannhom.csv
phannhom_file = './phannhom.csv'
df_original.to_csv(phannhom_file, index=False)

print(f"\nKết quả đã được lưu vào {phannhom_file}")




