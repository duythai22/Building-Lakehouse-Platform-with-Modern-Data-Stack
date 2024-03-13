import streamlit as st


def searchreviews(productname):
    # Đoạn mã ở đây để tìm kiếm review dựa trên tên sản phẩm
    # Ví dụ: Tìm kiếm trong cơ sở dữ liệu hoặc kết nối với API để nhận thông tin review
    # Trả về danh sách các review liên quan đến sản phẩm

    # Giả sử danh sách review đã được tìm kiếm
    reviews = ["Review 1", "Review 2", "Review 3"]

    return reviews


def main():
    # Tiêu đề ứng dụng
    st.title("Ứng dụng hiển thị review sản phẩm")

    # Người dùng nhập tên sản phẩm
    product_name = st.text_input("Nhập tên sản phẩm")

    # Kiểm tra xem người dùng đã nhập tên sản phẩm hay chưa
    if product_name:
        # Tìm kiếm review dựa trên tên sản phẩm
        reviews = searchreviews(product_name)

        # Hiển thị danh sách các review
        st.header("Các review của sản phẩm '{}'".format(product_name))
        for review in reviews:
            st.write(review)
    else:
        st.write("Vui lòng nhập tên sản phẩm.")


if __name__ == "__main__":
    main()
