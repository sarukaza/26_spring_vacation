create database spring_vacation;
use spring_vacation;

create table users(
    user_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    salt VARCHAR(64),
    password_hash VARCHAR(255)
);

create table books(
    book_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    genre VARCHAR(50),
    publication_year INTEGER
);

CREATE TABLE borrowed_books (
    transaction_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER,
    book_id INTEGER,
    borrow_date DATE,
    return_date DATE,
    returned BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

insert into books (title, author, genre, publication_year) values
('容疑者Xの献身', '東野圭吾', '小説', 2005),
('よつばと！', 'あずまきよひこ', '漫画',2003),
('進撃の巨人', '諫山創', '漫画', 2009),
('ハリー・ポッターと賢者の石', 'J.K.ローリング', '小説', 1997),
('ノルウェイの森', '村上春樹', '小説', 1987),
('ワンピース', '尾田栄一郎', '漫画', 1997),
('君の名は。', '新海誠', '小説', 2016),
('新世界より', '貴志祐介', '小説', 2008),
('バガボンド', '井上井恵', '漫画', 1998),
('GTO', '藤沢とおる', '漫画', 1997);