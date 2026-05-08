SET FOREIGN_KEY_CHECKS=0;

-- 1. Đổi Admin Vũ Văn X (ID 6) sang một ID tạm là 999
UPDATE Users SET UserID = 999 WHERE UserID = 6;
UPDATE BankAccounts SET UserID = 999 WHERE UserID = 6;
UPDATE Income SET UserID = 999 WHERE UserID = 6;
UPDATE Expenses SET UserID = 999 WHERE UserID = 6;

-- 2. Đổi User Nguyễn Văn A (ID 1) thành ID 6
UPDATE Users SET UserID = 6 WHERE UserID = 1;
UPDATE BankAccounts SET UserID = 6 WHERE UserID = 1;
UPDATE Income SET UserID = 6 WHERE UserID = 1;
UPDATE Expenses SET UserID = 6 WHERE UserID = 1;

-- 3. Đổi Admin Vũ Văn X từ ID tạm 999 về ID 1
UPDATE Users SET UserID = 1 WHERE UserID = 999;
UPDATE BankAccounts SET UserID = 1 WHERE UserID = 999;
UPDATE Income SET UserID = 1 WHERE UserID = 999;
UPDATE Expenses SET UserID = 1 WHERE UserID = 999;

-- 4. Cập nhật lại cột Role cho chuẩn xác
UPDATE Users SET Role = 'Admin' WHERE UserID = 1; -- Vũ Văn X làm Admin
UPDATE Users SET Role = 'User' WHERE UserID = 6;  -- Nguyễn Văn A làm User thường

SET FOREIGN_KEY_CHECKS=1;
