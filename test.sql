DROP TABLE server_pay;

CREATE Table server_pay (
    id_server TEXT PRIMARY KEY,
    is_pay BOOLEAN DEFAULT 0
)


SELECT id_server, is_pay FROM server_pay;
UPDATE server_pay SET is_pay=? WHERE id_server=?;

INSERT INTO server_pay(id_server, is_pay) VALUES (?, ?);

DELETE FROM server_pay WHERE id_server=?;

INSERT INTO server_pay(id_server, is_pay) VALUES (?, ?) 
ON CONFLICT(id_server) DO UPDATE SET is_pay = excluded.is_pay;


DROP TABLE qr_pay_code;
CREATE TABLE qr_pay_code (
    qr_code TEXT PRIMARY KEY,
    id_server TEXT,
    channel_id TEXT,
    message_id TEXT,
    ngay_tao DATETIME
)


SELECT qr_code, id_server, channel_id, message_id, ngay_tao FROM qr_pay_code WHERE qr_code=?; 

INSERT INTO qr_pay_code(qr_code, id_server, channel_id, message_id, ngay_tao) VALUES (?, ?, ?, ?, ?);

DELETE FROM qr_pay_code WHERE qr_code=?;




CREATE TABLE transaction_history (
    transaction_id TEXT PRIMARY KEY,
    `time` datetime,
    `content` TEXT,
    credit_amount INT,
    `currency` TEXT
)

SELECT transaction_id , `time`, `content`, credit_amount , `currency` FROM transaction_history WHERE transaction_id=?;

INSERT INTO transaction_history(transaction_id , `time`, `content`, credit_amount , `currency`) VALUES (?, ?, ?, ?, ?)



-- chỉnh lại các bot tạo database
-- thay toàn bộ print bằng logger
-- thêm 2 table một là server_pay nhữ server đã đăng ký vip, qr_pay_code lưu nhữ mã qr còn hạng