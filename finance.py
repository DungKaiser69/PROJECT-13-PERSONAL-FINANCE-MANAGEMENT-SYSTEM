import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import getpass
from sqlalchemy import create_engine, text, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# ==========================================
# CẤU HÌNH KẾT NỐI DATABASE
# ==========================================
# 1. BẢO PYTHON ĐỌC FILE .env
load_dotenv()

# 2. LẤY CHUỖI KẾT NỐI TỪ BIẾN MÔI TRƯỜNG
db_uri = os.getenv("DB_URI") 

# Nếu không tìm thấy file .env, báo lỗi ngay lập tức
if not db_uri:
    raise ValueError("❌ Không tìm thấy biến môi trường DB_URI. Hãy kiểm tra file .env!")

engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()

# Biến toàn cục để lưu phiên đăng nhập
CURRENT_USER_ID = None
CURRENT_USER_NAME = ""
IS_ADMIN = False

# ==========================================
# KHAI BÁO CÁC MODEL (ORM)
# ==========================================
Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    UserID = Column(Integer, primary_key=True)
    UserName = Column(String(100))
    Email = Column(String(100))
    PhoneNumber = Column(String(15))
    Password = Column(String(255))
    Role = Column(String(20))

class BankAccount(Base):
    __tablename__ = 'BankAccounts'
    AccountID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    BankName = Column(String(100))
    Balance = Column(Numeric(15, 2))

class ExpenseCategory(Base):
    __tablename__ = 'ExpenseCategories'
    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String(100))

class Income(Base):
    __tablename__ = 'Income'
    IncomeID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    AccountID = Column(Integer, ForeignKey('BankAccounts.AccountID'))
    Amount = Column(Numeric(15, 2))
    IncomeDate = Column(Date)
    Description = Column(String)

class Expense(Base):
    __tablename__ = 'Expenses'
    ExpenseID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    AccountID = Column(Integer, ForeignKey('BankAccounts.AccountID'))
    CategoryID = Column(Integer, ForeignKey('ExpenseCategories.CategoryID'))
    Amount = Column(Numeric(15, 2))
    ExpenseDate = Column(Date)
    Description = Column(String)


# ==========================================
# CÁC CHỨC NĂNG DÀNH RIÊNG CHO ADMIN
# ==========================================
def admin_view_users():
    """Secure user information with authentication roles."""
    print("\n--- 📋 QUẢN LÝ THÔNG TIN NGƯỜI DÙNG (ADMIN) ---")
    query = "SELECT UserID, UserName, Email, PhoneNumber FROM Users WHERE Role != 'Admin'"

    df = pd.read_sql(query, engine)
    print(df.to_markdown(index=False))

def admin_backup_database():
    """Ensure backup and recovery procedures are in place."""
    print("\n--- 💾 SAO LƯU DỮ LIỆU HỆ THỐNG (BACKUP) ---")
    tables = ['Users', 'BankAccounts', 'ExpenseCategories', 'Income', 'Expenses']
    
    # SỬA LỖI WINERROR 5: Tự động trỏ đường dẫn ra thẳng màn hình Desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    backup_dir = os.path.join(desktop_path, "database_backups")
    
    if not os.path.exists(backup_dir):
        try:
            os.makedirs(backup_dir)
        except Exception as e:
            print(f"❌ Không thể tạo thư mục Backup trên Desktop: {e}")
            return
            
    try:
        for table in tables:
            df = pd.read_sql(f"SELECT * FROM {table}", engine)
            df.to_csv(os.path.join(backup_dir, f"backup_{table}.csv"), index=False)
            
        print(f"✅ Đã sao lưu toàn bộ dữ liệu thành công!")
        print(f"📂 Bạn hãy ra màn hình Desktop, tìm thư mục: 'database_backups' để kiểm tra nhé!")
    except Exception as e:
        print(f"❌ Lỗi sao lưu: {e}")

def admin_optimize_database():
    """Optimize query performance for report generation."""
    print("\n--- 🚀 TỐI ƯU HÓA HIỆU SUẤT TRUY VẤN (OPTIMIZE) ---")
    try:
        # 1. Bắt buộc kết thúc các giao dịch ngầm cũ để nhả Khóa bảng (Release Locks)
        session.commit()
        
        # 2. Thực thi lệnh Optimize
        with engine.connect() as conn:
            # Chạy lệnh
            result = conn.execute(text("OPTIMIZE TABLE Users, BankAccounts, Expenses, Income, ExpenseCategories"))
            
            # 3. Yêu cầu Python đọc hết kết quả trả về để giải phóng hoàn toàn bộ nhớ
            result.fetchall()
            conn.commit()
            
        print("✅ Đã dọn dẹp phân mảnh và làm mới Index cho toàn bộ các bảng!")
        print("✅ Hiệu suất xuất báo cáo tài chính (Report Generation) đã được tối ưu đạt mức tối đa.")
    except Exception as e:
        print(f"❌ Lỗi tối ưu: {e}")

# ==========================================
# CHỨC NĂNG GIÁM SÁT DÀNH CHO ADMIN
# ==========================================
def admin_monitor_system_financials():
    """Chức năng xem toàn bộ số dư và lịch sử giao dịch toàn hệ thống"""
    print("\n--- 📊 GIÁM SÁT TÀI CHÍNH TOÀN HỆ THỐNG (ADMIN) ---")
    
    # Xem tổng hợp số dư các tài khoản
    print("\n[1] TỔNG HỢP SỐ DƯ TẤT CẢ NGƯỜI DÙNG:")
    query_bal = """
        SELECT u.UserName, b.BankName, b.Balance 
        FROM BankAccounts b 
        JOIN Users u ON b.UserID = u.UserID
    """
    df_bal = pd.read_sql(query_bal, engine)
    df_bal['Balance'] = df_bal['Balance'].astype(float)
    print(df_bal.to_markdown(index=False, floatfmt=",.0f"))

    # Xem toàn bộ lịch sử giao dịch gần đây
    print("\n[2] TOÀN BỘ GIAO DỊCH GẦN ĐÂY TRÊN HỆ THỐNG:")
    query_all_hist = """
        SELECT u.UserName, 'Chi tiêu' as Loai, e.Amount, e.ExpenseDate as Ngay, e.Description 
        FROM Expenses e JOIN Users u ON e.UserID = u.UserID
        UNION ALL
        SELECT u.UserName, 'Thu nhập' as Loai, i.Amount, i.IncomeDate as Ngay, i.Description 
        FROM Income i JOIN Users u ON i.UserID = u.UserID
        ORDER BY Ngay DESC LIMIT 20
    """
    df_hist = pd.read_sql(query_all_hist, engine)
    df_hist['Amount'] = df_hist['Amount'].astype(float)
    print(df_hist.to_markdown(index=False, floatfmt=",.0f"))

def admin_check_system_alerts():
    """Thông báo cho Admin những người dùng đang chi tiêu vượt mức hoặc có giao dịch lớn"""
    print("\n--- ⚠️ HỆ THỐNG CẢNH BÁO TRUNG TÂM (ADMIN) ---")
    threshold = 5000000 # Ngưỡng cảnh báo giao dịch lớn: 5 triệu
    
    # 1. Cảnh báo giao dịch lớn
    query_big_spent = f"SELECT u.UserName, e.Amount, e.Description FROM Expenses e JOIN Users u ON e.UserID = u.UserID WHERE e.Amount > {threshold}"
    df_big = pd.read_sql(query_big_spent, engine)
    
    if not df_big.empty:
        df_big['Amount'] = df_big['Amount'].astype(float)
        
        print(f"❗ PHÁT HIỆN {len(df_big)} GIAO DỊCH LỚN (> 5tr):")
        print(df_big.to_markdown(index=False, floatfmt=",.0f"))
    else:
        print("✅ Chưa có giao dịch bất thường nào.")


# ==========================================
# CÁC CHỨC NĂNG TÀI CHÍNH (CHỈ DÀNH CHO USER)
# ==========================================
def user_view_profile():
    print("\n--- 👤 HỒ SƠ CÁ NHÂN ---")
    user = session.query(User).filter(User.UserID == CURRENT_USER_ID).first()
    if user:
        print(f"ID: {user.UserID} | Tên: {user.UserName}")
        print(f"Email: {user.Email} | SĐT: {user.PhoneNumber}")

def user_entry_update_categorization():
    print("\n--- 2. QUẢN LÝ GIAO DỊCH (THÊM, SỬA, PHÂN LOẠI) ---")
    print("a. Thêm Thu nhập (Income)")
    print("b. Thêm Chi tiêu & Phân loại (Expense Categorization)")
    print("c. Cập nhật giao dịch chi tiêu (Update)")
    sub_choice = input("Chọn thao tác (a/b/c): ").lower()
    
    if sub_choice == 'a':
        print("\n* Danh Sách Tài Khoản Của Bạn:")
        acc_df = pd.read_sql(f"SELECT AccountID, BankName FROM BankAccounts WHERE UserID = {CURRENT_USER_ID}", engine)
        if acc_df.empty: 
            print("Bạn chưa có tài khoản ngân hàng!"); return
        print(acc_df.to_markdown(index=False))
        
        amount = float(input("\nNhập số tiền thu nhập (VND): "))
        account = int(input("Nhập ID tài khoản nhận tiền: "))
        date = input("Nhập ngày (YYYY-MM-DD): ")
        desc = input("Nhập mô tả: ")
        
        new_income = Income(UserID=CURRENT_USER_ID, AccountID=account, Amount=amount, IncomeDate=date, Description=desc)
        session.add(new_income)
        acc = session.query(BankAccount).filter(BankAccount.AccountID == account).first()
        if acc: acc.Balance = float(acc.Balance) + amount
        try:
            session.commit()
            print("✅ Thêm thu nhập thành công!")
        
        except Exception as e:
            session.rollback() # Hoàn tác nếu có lỗi
            print(f"❌ Lỗi: ID tài khoản không tồn tại hoặc dữ liệu không hợp lệ!")
        
    elif sub_choice == 'b':
        print("\n* Danh Sách Tài Khoản Của Bạn:")
        acc_df = pd.read_sql(f"SELECT AccountID, BankName FROM BankAccounts WHERE UserID = {CURRENT_USER_ID}", engine)
        print(acc_df.to_markdown(index=False))

        print("\n* Bảng Phân Loại Chi Tiêu:")
        cat_df = pd.read_sql("SELECT CategoryID, CategoryName FROM ExpenseCategories", engine)
        print(cat_df.to_markdown(index=False))
        
        amount = float(input("\nNhập số tiền (VND): "))
        account = int(input("Nhập ID tài khoản bị trừ tiền: "))
        category = int(input("Nhập ID danh mục: "))
        date = input("Nhập ngày (YYYY-MM-DD): ")
        desc = input("Nhập mô tả: ")
        
        query = f"INSERT INTO Expenses (UserID, AccountID, CategoryID, Amount, ExpenseDate, Description) VALUES ({CURRENT_USER_ID}, {account}, {category}, {amount}, '{date}', '{desc}')"
        with engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()
        print("✅ Đã lưu chi tiêu và cập nhật số dư!")
        
    elif sub_choice == 'c':
        print("\n* BẢNG GIAO DỊCH CHI TIÊU GẦN NHẤT:")
        query = f"SELECT ExpenseID, Amount, ExpenseDate, Description FROM Expenses WHERE UserID = {CURRENT_USER_ID} ORDER BY ExpenseDate DESC LIMIT 10"
        df = pd.read_sql(query, engine)
        if df.empty:
            print("Bạn chưa có giao dịch chi tiêu nào để sửa!"); return
        df['Amount'] = df['Amount'].astype(float)
        print(df.to_markdown(index=False, floatfmt=",.0f"))

        exp_id = int(input("\nNhập ExpenseID muốn sửa (Nhập 0 để hủy): "))
        if exp_id != 0:
            new_amount = float(input("Nhập số tiền MỚI (VND): "))
            with engine.connect() as conn:
                conn.execute(text(f"UPDATE Expenses SET Amount = {new_amount} WHERE ExpenseID = {exp_id} AND UserID = {CURRENT_USER_ID}"))
                conn.commit()
            print("✅ Đã cập nhật số tiền giao dịch thành công!")

def user_bank_tracking_history():
    print("\n--- 3. THEO DÕI TÀI KHOẢN VÀ LỊCH SỬ BIẾN ĐỘNG ---")
    query_acc = f"SELECT AccountID, BankName, Balance FROM BankAccounts WHERE UserID = {CURRENT_USER_ID}"
    df_acc = pd.read_sql(query_acc, engine)
    if not df_acc.empty:
        df_acc['Balance'] = df_acc['Balance'].astype(float)
        print("\n* SỐ DƯ HIỆN TẠI:")
        print(df_acc.to_markdown(index=False, floatfmt=",.0f"))
    
    query_history = f"""
        SELECT 'Income' AS Type, IncomeDate AS Date, Amount, Description FROM Income WHERE UserID = {CURRENT_USER_ID}
        UNION ALL
        SELECT 'Expense' AS Type, ExpenseDate AS Date, -Amount, Description FROM Expenses WHERE UserID = {CURRENT_USER_ID}
        ORDER BY Date DESC LIMIT 15
    """
    df_hist = pd.read_sql(query_history, engine)
    if not df_hist.empty:
        df_hist['Amount'] = df_hist['Amount'].astype(float)
        print("\n* LỊCH SỬ GIAO DỊCH CỦA BẠN:")
        print(df_hist.to_markdown(index=False, floatfmt=",.0f"))

def user_temporal_summaries():
    print("\n--- 4. TÓM TẮT TÀI CHÍNH ---")
    print("a. Theo ngày (Daily)")
    print("b. Theo tháng (Monthly)")
    print("c. Theo năm (Yearly)")
    choice = input("Chọn chế độ xem (a/b/c): ").lower()
    
    # a. THEO NGÀY: Dùng SQL gộp Thu/Chi bằng UNION ALL
    if choice == 'a': 
        query = f"""
            SELECT DATE_FORMAT(TransactionDate, '%Y-%m-%d') AS Period, TransactionType, SUM(Amount) AS TotalAmount
            FROM (
                SELECT UserID, IncomeDate AS TransactionDate, 'Income' AS TransactionType, Amount FROM Income
                UNION ALL
                SELECT UserID, ExpenseDate AS TransactionDate, 'Expense' AS TransactionType, Amount FROM Expenses
            ) AS CombinedData
            WHERE UserID = {CURRENT_USER_ID}
            GROUP BY Period, TransactionType
            ORDER BY Period DESC, TransactionType ASC
        """
        
    # b. THEO THÁNG: Gọi thẳng View trong Database
    elif choice == 'b': 
        query = f"""
            SELECT ReportMonth AS Period, TransactionType, TotalAmount 
            FROM MonthlyFinancialSummaryView 
            WHERE UserID = {CURRENT_USER_ID} 
            ORDER BY Period DESC, TransactionType ASC
        """
        
    # c. THEO NĂM: Dùng SQL gộp Thu/Chi bằng UNION ALL
    elif choice == 'c': 
        query = f"""
            SELECT YEAR(TransactionDate) AS Period, TransactionType, SUM(Amount) AS TotalAmount
            FROM (
                SELECT UserID, IncomeDate AS TransactionDate, 'Income' AS TransactionType, Amount FROM Income
                UNION ALL
                SELECT UserID, ExpenseDate AS TransactionDate, 'Expense' AS TransactionType, Amount FROM Expenses
            ) AS CombinedData
            WHERE UserID = {CURRENT_USER_ID}
            GROUP BY Period, TransactionType
            ORDER BY Period DESC, TransactionType ASC
        """
        
    else: 
        print("❌ Lựa chọn không hợp lệ! Vui lòng chọn a, b hoặc c.")
        return 
        
    df = pd.read_sql(query, engine)
    
    if not df.empty:
        df['TotalAmount'] = df['TotalAmount'].astype(float)
        print(f"\n* 📊 BÁO CÁO TỔNG HỢP THU/CHI CỦA BẠN:")
        print(df.to_markdown(index=False, floatfmt=",.0f"))
    else: 
        print("Bạn chưa có dữ liệu giao dịch nào.")

def user_budget_alerts():
    print("\n--- 5. KẾ HOẠCH NGÂN SÁCH & CẢNH BÁO CHI TIẾT ---")
    try:
        limit = float(input("Nhập hạn mức chi tiêu tháng này của bạn (VND): "))
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        
        query = f"SELECT SUM(Amount) FROM Expenses WHERE UserID = {CURRENT_USER_ID} AND MONTH(ExpenseDate) = {current_month} AND YEAR(ExpenseDate) = {current_year}"
        with engine.connect() as conn:
            result = conn.execute(text(query)).scalar()
            total_spent = float(result) if result else 0.0

        remaining = limit - total_spent
        percent = (total_spent / limit) * 100 if limit > 0 else 0

        print(f"\n📊 BÁO CÁO THÁNG {current_month}/{current_year}:")
        print(f"- Đã chi: {total_spent:,.0f} VND ({percent:.1f}%)")
        print(f"- Còn lại: {remaining:,.0f} VND")

        if percent >= 100:
            print("❌ CẢNH BÁO NGUY HIỂM: Bạn đã vượt hạn mức chi tiêu!")
        elif percent >= 80:
            print("⚠️ CẢNH BÁO VÀNG: Bạn đã tiêu quá 80%, hãy cân nhắc cắt giảm.")
        else:
            print("✅ AN TOÀN: Chi tiêu hiện tại vẫn nằm trong kế hoạch.")
            
    except ValueError:
        print("❌ Lỗi: Vui lòng nhập số tiền hợp lệ!")

def user_report_spending_trend():
    print("\n--- 6. BÁO CÁO XU HƯỚNG CHI TIÊU ---")
    query_daily = f"SELECT DATE_FORMAT(ExpenseDate, '%Y-%m-%d') AS Date, SUM(Amount) AS TotalSpent FROM Expenses WHERE UserID = {CURRENT_USER_ID} GROUP BY Date ORDER BY Date ASC"
    df_daily = pd.read_sql(query_daily, engine)
    
    query_monthly = f"SELECT DATE_FORMAT(ExpenseDate, '%Y-%m') AS Month, SUM(Amount) AS TotalSpent FROM Expenses WHERE UserID = {CURRENT_USER_ID} GROUP BY Month ORDER BY Month ASC"
    df_monthly = pd.read_sql(query_monthly, engine)

    if df_daily.empty and df_monthly.empty:
        print("Bạn chưa có dữ liệu để vẽ biểu đồ.")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    if not df_daily.empty:
        ax1.plot(df_daily['Date'], df_daily['TotalSpent'], marker='o', color='#2ca02c')
        ax1.set_title('Daily Spending Trend', fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, linestyle='--')

    if not df_monthly.empty:
        ax2.plot(df_monthly['Month'], df_monthly['TotalSpent'], marker='s', color='#d62728')
        ax2.set_title('Monthly Spending Trend', fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, linestyle='--')

    plt.tight_layout()
    plt.show()

def user_report_category():
    print("\n--- 7. BÁO CÁO CHI TIÊU THEO DANH MỤC ---")
    query_cat = f"""
        SELECT c.CategoryName, SUM(e.Amount) AS TotalSpent 
        FROM Expenses e 
        JOIN ExpenseCategories c ON e.CategoryID = c.CategoryID 
        WHERE e.UserID = {CURRENT_USER_ID} 
        GROUP BY c.CategoryName
    """
    df_cat = pd.read_sql(query_cat, engine)

    if df_cat.empty:
        print("Bạn chưa có dữ liệu để vẽ biểu đồ.")
        return

    plt.figure(figsize=(8, 6))
    bars = plt.bar(df_cat['CategoryName'], df_cat['TotalSpent'], color='#4C72B0', edgecolor='black')
    plt.title('Expenditure by Category', fontweight='bold')
    plt.tick_params(axis='x', rotation=45)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + (yval*0.02), f'{yval:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()

def user_monthly_closure():
    print("\n--- 📝 CHỐT SỔ TÀI CHÍNH CUỐI THÁNG ---")
    try:
        month = int(input("Nhập THÁNG cần chốt sổ (1-12): "))
        year = int(input("Nhập NĂM cần chốt sổ (YYYY): "))
        
        # Gọi thủ tục lưu trữ từ MySQL
        query = f"CALL MonthlyClosure({CURRENT_USER_ID}, {month}, {year})"
        df = pd.read_sql(query, engine)
        
        print("\n✅ KẾT QUẢ CHỐT SỔ TỪ DATABASE:")
        print(df.to_markdown(index=False, floatfmt=",.0f"))
    except Exception as e:
        print(f"❌ Lỗi: Vui lòng nhập số hợp lệ! Chi tiết: {e}")

# ==========================================
# HỆ THỐNG ĐĂNG NHẬP (SECURE AUTHENTICATION)
# ==========================================
def login_system():
    global CURRENT_USER_ID, CURRENT_USER_NAME, IS_ADMIN
    while True:
        print("\n" + "="*55)
        print(" ĐĂNG NHẬP HỆ THỐNG (BẢO MẬT CẤP CAO) ")
        print("="*55)
        try:
            # Yêu cầu nhập Email thay vì ID
            email = input("📧 Nhập Email đăng nhập: ").strip()
            
            # getpass giúp ẩn ký tự khi gõ mật khẩu (chống nhìn trộm)
            password = getpass.getpass("🔑 Nhập Mật khẩu (ký tự sẽ bị ẩn): ").strip()
            
            # Truy vấn kiểm tra khớp cả Email và Mật khẩu
            user = session.query(User).filter(User.Email == email, User.Password == password).first()
            
            if user:
                CURRENT_USER_ID = user.UserID
                CURRENT_USER_NAME = user.UserName
                IS_ADMIN = (user.Role.lower() == "admin") if user.Role else False
                
                role_icon = "👑 ADMIN" if IS_ADMIN else "👤 USER"
                print(f"\n✅ Xác thực thành công! Xin chào {CURRENT_USER_NAME} ({role_icon})")
                break
            else:
                print("❌ Đăng nhập thất bại: Sai Email hoặc Mật khẩu!")
        except Exception as e:
            print(f"Lỗi Database: {e}"); break


# ==========================================
# MENU CHÍNH
# ==========================================
if __name__ == "__main__":
    login_system()
    
    while True:
        print("\n" + "="*65)
        print(f" HỆ THỐNG QUẢN LÝ | User: {CURRENT_USER_NAME} | Quyền: {'Admin' if IS_ADMIN else 'User'} ")
        print("="*65)
        
        if IS_ADMIN:
            # MENU ADMIN CẬP NHẬT
            print("1. Quản lý danh sách người dùng")
            print("2. Sao lưu dữ liệu hệ thống (Backup)")
            print("3. Tối ưu hóa hiệu suất")
            print("4. Giám sát tài chính & Số dư toàn hệ thống")
            print("5. Xem cảnh báo giao dịch bất thường")
            print("6. Đăng xuất")
            
            choice = input("\nChọn chức năng (1-6): ")
            if choice == '1': admin_view_users()
            elif choice == '2': admin_backup_database()
            elif choice == '3': admin_optimize_database()
            elif choice == '4': admin_monitor_system_financials()
            elif choice == '5': admin_check_system_alerts()
            elif choice == '6': break
            else: print("Lựa chọn không hợp lệ!")
            
        else:
            # MENU DÀNH CHO USER THƯỜNG
            print("1. Xem hồ sơ cá nhân")
            print("2. Nhập, cập nhật và phân loại thu/chi")
            print("3. Theo dõi tài khoản ngân hàng và lịch sử số dư")
            print("4. Tóm tắt tài chính theo ngày, tháng, năm")
            print("5. Lập kế hoạch ngân sách và cảnh báo chi tiêu")
            print("6. Báo cáo đồ thị xu hướng chi tiêu theo thời gian")
            print("7. Báo cáo đồ thị chi tiêu theo danh mục")
            print("8. Chốt sổ cuối tháng")
            print("9. Đăng xuất / Thoát hệ thống")
            
            choice = input("\nChọn chức năng (1-9): ")
            if choice == '1': user_view_profile()
            elif choice == '2': user_entry_update_categorization()
            elif choice == '3': user_bank_tracking_history()
            elif choice == '4': user_temporal_summaries()
            elif choice == '5': user_budget_alerts()
            elif choice == '6': user_report_spending_trend()
            elif choice == '7': user_report_category()
            elif choice == '8': user_monthly_closure() 
            elif choice == '9': print("Đã đăng xuất!"); session.close(); break
            else: print("Lựa chọn không hợp lệ!")