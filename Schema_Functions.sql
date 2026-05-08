-- ==========================================
-- 4. CÁC ĐỐI TƯỢNG DATABASE NÂNG CAO
-- ==========================================

-- 4.1 Indexes: Tối ưu tìm kiếm theo ngày chi tiêu
CREATE INDEX idx_expense_date ON Expenses(ExpenseDate);

-- 4.2 Views: Khung nhìn tổng hợp chi tiêu theo danh mục
CREATE VIEW CategorySpendingView AS
SELECT c.CategoryName, SUM(e.Amount) as TotalSpent
FROM Expenses e
JOIN ExpenseCategories c ON e.CategoryID = c.CategoryID
GROUP BY c.CategoryName;

-- 4.3 Triggers: Tự động trừ tiền khi thêm chi tiêu mới
DELIMITER //
CREATE TRIGGER AfterExpenseInsert
AFTER INSERT ON Expenses
FOR EACH ROW
BEGIN
    UPDATE BankAccounts 
    SET Balance = Balance - NEW.Amount 
    WHERE AccountID = NEW.AccountID;
END; //
DELIMITER ;

-- 4.4 Triggers: Tự động hoàn tiền khi xóa chi tiêu (Tính năng bảo vệ dữ liệu)
DELIMITER //
CREATE TRIGGER AfterExpenseDelete
AFTER DELETE ON Expenses
FOR EACH ROW
BEGIN
    UPDATE BankAccounts 
    SET Balance = Balance + OLD.Amount 
    WHERE AccountID = OLD.AccountID;
END; //
DELIMITER ;

-- 4.5 User Defined Functions: Tính tổng chi tiêu của một người dùng cụ thể
DELIMITER //
CREATE FUNCTION GetTotalExpenseByUser(p_UserID INT) 
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(15,2);
    SELECT IFNULL(SUM(Amount), 0) INTO total FROM Expenses WHERE UserID = p_UserID;
    RETURN total;
END; //
DELIMITER ;

-- 4.6 Views: Khung nhìn tổng hợp Thu/Chi theo tháng
CREATE VIEW MonthlyFinancialSummaryView AS
SELECT 
    UserID,
    DATE_FORMAT(TransactionDate, '%Y-%m') AS ReportMonth,
    TransactionType,
    SUM(Amount) AS TotalAmount
FROM (
    SELECT UserID, IncomeDate AS TransactionDate, 'Income' AS TransactionType, Amount FROM Income
    UNION ALL
    SELECT UserID, ExpenseDate AS TransactionDate, 'Expense' AS TransactionType, Amount FROM Expenses
) AS CombinedData
GROUP BY UserID, ReportMonth, TransactionType;

-- 4.7 Stored Procedures: Thủ tục chốt sổ hàng tháng
DELIMITER //
CREATE PROCEDURE MonthlyClosure(IN p_UserID INT, IN p_Month INT, IN p_Year INT)
BEGIN
    SELECT 
        p_Month AS 'Tháng',
        p_Year AS 'Năm',
        (SELECT IFNULL(SUM(Amount), 0) FROM Income WHERE UserID = p_UserID AND MONTH(IncomeDate) = p_Month AND YEAR(IncomeDate) = p_Year) AS 'Tổng Thu',
        (SELECT IFNULL(SUM(Amount), 0) FROM Expenses WHERE UserID = p_UserID AND MONTH(ExpenseDate) = p_Month AND YEAR(ExpenseDate) = p_Year) AS 'Tổng Chi',
        (SELECT SUM(Balance) FROM BankAccounts WHERE UserID = p_UserID) AS 'Tổng Số Dư Hiện Tại';
END; //
DELIMITER ;
