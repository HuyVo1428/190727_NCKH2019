TẠO MÔI TRƯỜNG
1. Install đầy đủ phiên bản mới nhất của openwpm
2. Copy toàn bộ thư mục openwpm vừa install thành công vào thư mục này (cùng cấp với file_for_openwpm)
3. Copy toàn bộ các file trong file_for_openwpm vào thư mục openwpm vừa thêm

4. Install đầy đủ các thư viện 
flask
requests
và các thư viện dùng trong code


CHẠY CHƯƠNG TRÌNH
1. Chạy <python3 flask_api.py> trong thư mục openwpm sau khi hoàn thành tạo môi trường
2. Có thể kết hợp chạy với ngrok ở port 5000
tải và cài đặt tại: https://ngrok.com/

Hiện tại có thể giao tiếp với hệ thống thông qua POST request đến địa chỉ máy chủ (local hoặc public của ngrok) với json format {"domain":"<domain cần quét>"}

VÍ DỤ: curl -i -H "Content-Type: application/json" -X POST -d '{"domain":"http://tuoitre.vn"}' https://65d7de85.ngrok.io
