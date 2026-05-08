-- ==========================================
-- 1. KHỞI TẠO CƠ SỞ DỮ LIỆU
-- ==========================================
DROP DATABASE IF EXISTS PersonalFinance;
CREATE DATABASE PersonalFinance;
USE PersonalFinance;

-- ==========================================
-- 2. TẠO CẤU TRÚC BẢNG (TABLE STRUCTURES)
-- ==========================================
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(15)
);

CREATE TABLE BankAccounts (
    AccountID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    BankName VARCHAR(100) NOT NULL,
    Balance DECIMAL(15, 2) DEFAULT 0.00,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE TABLE ExpenseCategories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL
);

CREATE TABLE Income (
    IncomeID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    AccountID INT,
    Amount DECIMAL(15, 2) NOT NULL,
    IncomeDate DATE NOT NULL,
    Description TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (AccountID) REFERENCES BankAccounts(AccountID) ON DELETE CASCADE
);

CREATE TABLE Expenses (
    ExpenseID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    AccountID INT,
    CategoryID INT,
    Amount DECIMAL(15, 2) NOT NULL,
    ExpenseDate DATE NOT NULL,
    Description TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (AccountID) REFERENCES BankAccounts(AccountID) ON DELETE CASCADE,
    FOREIGN KEY (CategoryID) REFERENCES ExpenseCategories(CategoryID) ON DELETE SET NULL
);
