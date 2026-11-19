1. Thiết kế chuỗi Prompt (3 bước khép kín)
B1 (Feynman + Socratic): Chẩn đoán lỗ hổng hiểu biết và đặt tối đa 1 câu hỏi gợi mở, không đưa đáp án sẵn, không nịnh hót.

B2 (Chấm Rubric): Chấm điểm theo tiêu chí có trọng số (Bản chất 40%, Ẩn dụ/Lập luận 30%, Chính xác/Đầy đủ 30%) dựa trên bằng chứng thực tế.

B3 (Actionable Feedback): Xuất lỗi cụ thể, cách sửa từng bước và bước luyện tập tiếp theo, bỏ lời chào/kết thừa.

2. Prompt thực thi
Prompt 1: Gia sư Feynman và Socratic cho chủ đề [TOPIC]. Tìm lỗ hổng và đặt tối đa 1 câu hỏi gợi mở (không đáp án sẵn, không nịnh hót, tối đa 3 gạch đầu dòng). Giải thích: [INPUT]

Prompt 2: Chấm Rubric (Bản chất 40, Ẩn dụ và Lập luận 30, Chính xác và Đầy đủ 30) khách quan, không nịnh hót. Trả về đúng 4 dòng (3 tiêu chí + Tổng). Input: [INPUT] | B1: [STEP1]

Prompt 3: Mentor học tập. Không chào/kết thừa. Trả về đúng 3 gạch đầu dòng: Lỗi cần sửa, Cách sửa, Bước tiếp theo. Dữ liệu: [STEP1] | [STEP2]

3. Code gọn (chặn lỗi và tối ưu token)
Python
def run_chain(topic: str, text: str, call_llm) -> dict:
    clean_t = str(topic or "").strip()[:100] or "Chủ đề"
    clean_x = str(text or "").strip()[:1200]
    if not clean_x:
        return {"ok": False, "err": "EMPTY_INPUT", "msg": "Thiếu nội dung giải thích để xử lý."}
    try:
        s1 = str(call_llm(f"Feynman/Socratic [{clean_t}]. Max 3 ý, <=1 câu hỏi gợi mở, không đáp án sẵn: {clean_x}") or "")[:600]
        s2 = str(call_llm(f"Chấm Rubric (40/30/30), 4 dòng (3 mục + Tổng), khách quan. Input: {clean_x} | S1: {s1}") or "")[:600]
        s3 = str(call_llm(f"3 gạch đầu dòng: Lỗi cần sửa, Cách sửa, Bước tiếp theo (không chào/kết). S1: {s1} | S2: {s2}") or "")[:600]
        return {"ok": True, "step1": s1, "step2": s2, "step3": s3}
    except Exception as e:
        return {"ok": False, "err": type(e).__name__, "msg": "Lỗi xử lý chuỗi prompt, vui lòng thử lại."}
4. Kết quả chạy thử sạch lỗi
Input: Chủ đề Đệ quy — "Hàm gọi lại chính nó, giống gương soi gương, chưa rõ khi nào dừng."

Bước 1: Ví dụ gương soi trực quan; lỗ hổng nằm ở điều kiện dừng. Điều kiện nào giúp hàm thoát đệ quy thay vì lặp vô hạn?

Bước 2: Bản chất (25/40) | Ẩn dụ và Lập luận (22/30) | Chính xác & Đầy đủ (18/30) | Tổng: 65/100.

Bước 3: Lỗi cần sửa: Thiếu điều kiện dừng (base case) và cập nhật trạng thái. Cách sửa: Thêm điều kiện thoát rõ ràng trước lời gọi đệ quy. Bước tiếp theo: Viết ví dụ tính giai thừa kèm điều kiện dừng.