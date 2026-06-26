def build_message(bank, action):

    if action == "maintenance":
        return (
            f"<b>🏦 Ngân hàng {bank}</b>\n\n"
            "🔴 <b>ĐANG BẢO TRÌ</b>\n\n"
            "Vui lòng không thực hiện giao dịch."
        )

    if action == "online":
        return (
            f"<b>🏦 Ngân hàng {bank}</b>\n\n"
            "✅ <b>HOÀN TẤT BẢO TRÌ</b>"
        )

    if action == "transfer":
        return (
            f"<b>🏦 Ngân hàng {bank}</b>\n\n"
            "⚠️ LỖI CHUYỂN KHOẢN"
        )

    if action == "qr":
        return (
            f"<b>🏦 Ngân hàng {bank}</b>\n\n"
            "⚠️ LỖI QR"
        )

    return bank