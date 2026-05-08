USE PersonalFinance;

-- Thêm cột Password vào bảng Users
ALTER TABLE Users ADD COLUMN Password VARCHAR(255);

-- Cài đặt mật khẩu cho Admin (Vũ Văn X)
UPDATE Users 
SET UserName = 'Vu Van X' 
WHERE Email = 'x.vu@gmail.com';
UPDATE Users SET Password = 'adminpassword' WHERE Email = 'x.vu@gmail.com';

-- Cập nhật mật khẩu mới cho Admin Vu Van X
UPDATE Users 
SET Password = 'admin' 
WHERE UserID = 6;

-- Cài đặt mật khẩu cho User thường (Trần Thị B và Lê Văn C)
UPDATE Users SET Password = 'user123' WHERE Email = 'a.nguyen@gmail.com';
UPDATE Users SET Password = 'user123' WHERE Email = 'b.tran@gmail.com';
UPDATE Users SET Password = 'user123' WHERE Email = 'c.le@gmail.com';

-- Cập nhật mật khẩu cho Phan Van D (ID: 4)
UPDATE Users 
SET Password = 'user123' 
WHERE Email = 'd.phan@gmail.com';

-- Cập nhật mật khẩu cho Hoang Thi E (ID: 5)
UPDATE Users 
SET Password = 'user123' 
WHERE Email = 'e.hoang@gmail.com';
