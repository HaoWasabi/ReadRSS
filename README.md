# Aiko (ReadRSS)
This is a Discord bot built with Python, Aiko brings RSS feeds to your Discord server. Receive notifications from news sources including Facebook and much more. 
This is link to invite Aiko bot:
```
https://discord.com/oauth2/authorize?client_id=1236720788187381760&permissions=0&integration_type=0&scope=bot
```

```
                        -- ABOUT US --
                                                       Summer 2024
         ██████╗  ██████╗██████╗ ███████╗██╗   ██╗     + HaoWasabi
        ██╔════╝ ██╔════╝██╔══██╗██╔════╝██║   ██║     + nguyluky
        ██║  ███╗██║     ██║  ██║█████╗  ██║   ██║     + NaelTuhline
        ██║   ██║██║     ██║  ██║██╔══╝  ╚██╗ ██╔╝     + tivibin789
        ╚██████╔╝╚██████╗██████╔╝███████╗ ╚████╔╝      + phusomnia
        ╚═════╝  ╚═════╝╚═════╝ ╚══════╝  ╚═══╝        + camdao
``` 
## Installation
1. Clone the repository
2. Create a virtual environment and activate it
3. Install the dependencies: `pip install -r requirements.txt`
4. Create a `.env` file and add some information:
```
DISCORD_TOKEN=your_bot_token_here
GENMINI_TOKEN=your_api_gemini_token_here
QR_TEMPLATE=your_qr_template
BANK_ID=your_id_mbank_account
BANK_USER_NAME=your_name_mbank_account
BANK_PASSWORD=your_password_mbank_account
```

5. Run the bot: `python main.py`

## Basic slash_commands
Cách sử dụng các lệnh cơ bản:
+ `/getrss url:<url web>` hoặc `_getrss <url web>`: kiểm tra xem trang web đó có tồn tại link rss không.
+ `/test`: gửi thử bài đăng đầu tiên của trang web fit.sgu
+ `/test url:<url web>`: gửi thử bài đăng đầu tiên của trang web bất kì có tồn tại link rss bằng url web.
+ `/test rss:<link rss>` hoặc `_test <link rss>`: gửi thử bài đăng đầu tiên của trang web bất kì bằng link rss của trang web.
+ `/setfeed channel:<chọn kênh text> url:<url web> ` : thiết lập kênh để gửi bài đăng mới từ trang web bằng url web.
+ `/setfeed channel:<chọn kênh text> rss:<link rss> ` hoặc `_setfeed <chọn kênh text> <link rss> `: thiết lập kênh để gửi bài đăng mới từ trang web bằng link rss web.
+ `/deletefeed channel:<channel>` hoặc `_deletefeed <channel>`: Hủy thiết lập toàn bộ các thông báo các trang web đã đăng ký ở kênh chỉ định.
+ `/deletefeed channel:<channel> url:<url web>`: Hủy thiết lập thông báo của trang web có url đó đã đăng ký ở kênh chỉ định.
+ `/deletefeed channel:<channel> rss:<link rss>` hoặc `_deletefeed <channel> <link rss>`: Hủy thiết lập thbot báo của trang web có link rss đó đã đăng ký ở kênh chỉ định.
+ `/setcolor <chọn màu>` hoặc `_setcolor <tên màu ghi thường>`: thiết lập màu mặc định cho các embed mà bot sẽ gửi. Chỉ dùng được các màu đã lưu sẵn trong csdl như: yellow, red, blue, green, gray, black, puple
+ `_premium`: đăng kí gói vip, mở khóa tin năng có thể thiết lập các lệnh khi nhắn riêng cho bot(DMChannel). Người dùng không đăng kí gói vip chỉ được dùng các lệnh ở channel của server, không thể thiết lập khi nhắn riêng. Lưu ý: mở khóa premium sau khi chuyển khoản thành công tiền thật, sau 1p dữ liệu chuyển khoản sẽ được bot nhận được và lưu vào database rồi mở khóa. Sau 3p, tin nhắn tự thu hồi. Người dùng chọn button chứa tên các gói để bot tạo mã QR mang mệnh giá tương ứng. Chức năng giao dịch của bot làm ra với mục đích chuyển khoản tiền thật.
+ `checkpremium`: kiểm tra bản thân người dùng đã đăng kí gói premium chưa
+ `@<tên bot> <câu hỏi>`: hỏi để bot giao tiếp trả lời như chatgpt

**Lưu ý**: 
các lệnh setfeed, setcolor, deletefeed, showfeed có thể sử dụng miễn phí tại các kênh thuộc server, nhưng phải nâng cấp gói premium để có thể sử dụng tại DMChannel. 
Các lệnh còn có thể sử dụng tại tòan bộ các kênh trừ lệnh `_premium`.
Lệnh `_premium` chỉ có thể sử dụng tại kênh TextChannel của các server.


## Admin commands
Cách sử dụng các lệnh của ownerbot:
- `_shutdown`: tắt nguồn bot
- `_ctrl`: mở control panel, hiển thị các lệnh con để thao tác quản lý bot. Các lệnh con tiêu biểu:

        + Button “Shutdown”: Khi nhấn vào sẽ tắt nguồn bot.
        + Button “Show setting”: Khi nhấn vào sẽ hiển thị danh sách các kênh đã đăng kí nhận thông báo bài đăng mới từ các trang web chỉ định do user thiết lập
        + Button “Show servers”: Hiển thị danh sách các server mà bot đang tham gia.
        + Select “Clear”: Khi nhấn vào sẽ hiện thị các tùy chọn, tương ứng với mỗi lệnh con liên quan đến xoá, ẩn trong database
**Lưu ý**: Trong các modal hiện lên sau khi nhấn vào các lựa chọn. Các ô nhập input có dấu * màu đỏ là ô nhập không được để trống.

## Gemini commands
+ `@Aiko <câu hỏi của bạn>` # Bạn hỏi và bot có thể trả lời tương tự Gemini

## Other information
Đồ án được xây dựng theo mô hình 3 lớp mở rộng. Trong đó:
+ dal: xử lý logic truy cập dữ liệu.
+ bll: xử lý logic các yêu cầu từ lớp trình bày.
+ gui: xử lý giao diện
+ dto: chứa các lớp dùng để chuyển dữ liệu giữa các lớp hoặc tầng khác nhau. Mỗi lớp dto chứa có chứa các thuộc tính của các thực thể và các mối quan hệ.
+ utils: chứa các tệp tiện ích hoặc các hàm hỗ trợ mở rộng.
+ cogs: chứa các hàm sự kiện, lệnh bất đồng bộ tương tác với người dùng.


Các lỗi có thể xảy ra:
+ Dữ liệu trang web đã được nạp vào database của botchat. Sau 10s bot sẽ reload lại đọc đường link rss của các trang web. Nếu có bài đăng mới, ngay lập tức bot sẽ tự thông báo bài đăng đó đến kênh user đã chỉ định để nhận bài đăng từ trang web.
+ Bot có thể không hoạt động trong điều kiện đường truyền kết nối internet không thuận lợi. Hoặc phản hồi rất lâu, trong trường hợp đó nên ưu tiên sử dụng các lệnh command (vd: _ping) thay vì lệnh slash command (vd: /ping) vì chúng có thể phản hồi lâu, nhưng cũng sẽ không dùng được nếu đường truyền mạng quá yếu. 
