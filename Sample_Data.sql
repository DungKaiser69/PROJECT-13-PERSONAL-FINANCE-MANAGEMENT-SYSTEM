-- ==========================================
-- 3. NHẬP DỮ LIỆU MẪU (10 SAMPLE DATA)
-- ==========================================
-- Nhập 5 Users
INSERT INTO Users (UserName, Email, PhoneNumber, Password) VALUES
('Nguyen Van A', 'a.nguyen@gmail.com', '0912345678', 'user123'),
('Tran Thi B', 'b.tran@gmail.com', '0987654321', 'user123'),
('Le Van C', 'c.le@gmail.com', '0909090909', 'user123'),
('Phan Van D', 'd.phan@gmail.com', '0933445566', 'user123'),
('Hoang Thi E', 'e.hoang@gmail.com', '0944556677', 'user123');

-- Nhập 1 Admins:
INSERT INTO Users (UserName, Email, PhoneNumber, Password)
VALUES (6, 'Vu Van X', 'x.vu@gmail.com', '0911223344', 'admin');

-- Nhập 3 Bank Accounts (Số dư ban đầu)
INSERT INTO BankAccounts (UserID, BankName, Balance) VALUES 
(1, 'Vietcombank', 15000000),
(1, 'Techcombank', 5000000),
(2, 'BIDV', 20000000);
(4, 'ACB', 15000000),
(5, 'TPBank', 8000000);

-- Nhập 5 Expense Categories
INSERT INTO ExpenseCategories (CategoryName) VALUES 
('Food & Beverage'), 
('Transportation'), 
('Housing'), 
('Entertainment'), 
('Health & Fitness');

-- Nhập 10 Bản ghi Thu nhập (Income)
INSERT INTO Income (UserID, AccountID, Amount, IncomeDate, Description) VALUES 
(1, 1, 15000000, '2026-01-05', 'Salary January'),
(1, 2, 2000000, '2026-01-10', 'Freelance Web Design'),
(2, 3, 20000000, '2026-01-05', 'Salary January'),
(1, 1, 15000000, '2026-02-05', 'Salary February'),
(2, 3, 20000000, '2026-02-05', 'Salary February'),
(2, 3, 5000000, '2026-02-15', 'Year-end Bonus'),
(1, 1, 15000000, '2026-03-05', 'Salary March'),
(1, 2, 3000000, '2026-03-12', 'Stock Dividend'),
(2, 3, 20000000, '2026-03-05', 'Salary March'),
(2, 3, 1500000, '2026-03-20', 'Sold old bicycle');
(3, 3, 12000000, '2026-04-01', 'Luong thang 4'), 
(4, 4, 15000000, '2026-04-05', 'Bonus du an'),    
(5, 5, 7000000, '2026-04-10', 'Ban hang online'); 

-- Nhập 10 Bản ghi Chi tiêu (Expenses)
INSERT INTO Expenses (UserID, AccountID, CategoryID, Amount, ExpenseDate, Description) VALUES 
(1, 1, 1, 500000, '2026-03-01', 'Highlands Coffee & Dinner'),
(1, 1, 3, 4000000, '2026-03-05', 'Apartment Rent'),
(1, 2, 2, 150000, '2026-03-08', 'Grab Car to Office'),
(2, 3, 1, 1200000, '2026-03-10', 'Grocery shopping at Winmart'),
(2, 3, 4, 800000, '2026-03-12', 'Netflix and Spotify Subscription'),
(1, 1, 5, 600000, '2026-03-15', 'Pharmacy & Vitamins'),
(2, 3, 3, 5000000, '2026-03-16', 'House Rent'),
(1, 2, 2, 50000, '2026-03-18', 'Bus Tickets'),
(2, 3, 1, 350000, '2026-03-22', 'Weekend BBQ'),
(1, 1, 4, 250000, '2026-03-25', 'Cinema Tickets CGV');

-- Người C (ID: 3)
(3, 3, 1, 150000, '2026-04-15', 'An toi nha hang'),
(3, 3, 4, 500000, '2026-04-20', 'Xem phim & Shopping'),

-- Người D (ID: 4)
(4, 4, 3, 4500000, '2026-04-01', 'Tien thue chung cu'),
(4, 4, 2, 200000, '2026-04-10', 'Do xang xe oto'),
(4, 4, 1, 1200000, '2026-04-25', 'Di cho ca tuan'),

-- Người E (ID: 5)
(5, 5, 1, 50000, '2026-04-12', 'An sang'),
(5, 5, 4, 1500000, '2026-04-18', 'Mua khoa hoc online'),
(5, 5, 2, 100000, '2026-04-22', 'Nap the xe bus');
