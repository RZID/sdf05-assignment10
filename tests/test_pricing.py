import pytest

from pricing import (
    MEMBER_DISCOUNT_RATE,
    TAX_RATE,
    add_tax,
    apply_member_discount,
    calculate_subtotal,
    calculate_total,
    write_receipt,
)


# Aturan 1: subtotal = harga satuan x kuantitas
@pytest.mark.parametrize(
    "unit_price, quantity, expected",
    [
        (100, 2, 200),
        (0, 5, 0),
        (1500, 1, 1500),
        (10.5, 4, 42.0),
        (19.99, 3, 59.97),
    ],
)
def test_calculate_subtotal(unit_price, quantity, expected):
    assert calculate_subtotal(unit_price, quantity) == pytest.approx(expected)


def test_subtotal_zero_unit_price_returns_zero():
    assert calculate_subtotal(0, 10) == 0


# Aturan 2: harga negatif ditolak
def test_subtotal_negative_unit_price_raises():
    with pytest.raises(ValueError, match="unit_price must not be negative"):
        calculate_subtotal(-1, 2)


# Aturan 3: kuantitas nol / negatif ditolak
def test_subtotal_zero_quantity_raises():
    with pytest.raises(ValueError, match="quantity must be positive"):
        calculate_subtotal(100, 0)


def test_subtotal_negative_quantity_raises():
    with pytest.raises(ValueError, match="quantity must be positive"):
        calculate_subtotal(100, -3)


# Aturan 4: diskon 10% khusus anggota
def test_apply_member_discount_member_gets_ten_percent():
    assert apply_member_discount(1000, True) == pytest.approx(900.0)
    assert apply_member_discount(250.5, True) == pytest.approx(250.5 * (1 - MEMBER_DISCOUNT_RATE))


def test_apply_member_discount_nonmember_pays_full():
    assert apply_member_discount(1000, False) == pytest.approx(1000.0)
    assert apply_member_discount(250.5, False) == pytest.approx(250.5)


def test_apply_member_discount_zero_subtotal():
    assert apply_member_discount(0, True) == 0
    assert apply_member_discount(0, False) == 0


# Aturan 5: pajak 11% di atas nilai setelah diskon
def test_add_tax_eleven_percent():
    assert add_tax(100) == pytest.approx(111.0)
    assert add_tax(90) == pytest.approx(99.9)
    assert add_tax(0) == 0
    assert TAX_RATE == pytest.approx(0.11)


def test_calculate_total_nonmember():
    # (10000 * 2) * 1.11 = 22200
    assert calculate_total(10000, 2, is_member=False) == pytest.approx(22200.0)


def test_calculate_total_member():
    # (10000 * 2) * 0.9 * 1.11 = 19980
    assert calculate_total(10000, 2, is_member=True) == pytest.approx(19980.0)
    assert calculate_total(100, 2, is_member=True) == pytest.approx((200 * 0.9) * 1.11)


def test_calculate_total_propagates_input_validation():
    with pytest.raises(ValueError):
        calculate_total(-50, 2)
    with pytest.raises(ValueError):
        calculate_total(50, 0)


# Aturan 6: struk — tiap baris diakhiri newline, termasuk terakhir
def test_write_receipt_content_and_trailing_newline(tmp_path):
    target = tmp_path / "receipt.txt"
    lines = ["subtotal: 200", "diskon: 20", "total: 199.8"]
    write_receipt(str(target), lines)
    content = target.read_text(encoding="utf-8")
    assert content == "subtotal: 200\ndiskon: 20\ntotal: 199.8\n"
    assert content.endswith("\n")
    assert content.count("\n") == len(lines)


def test_write_receipt_single_line_and_overwrite(tmp_path):
    target = tmp_path / "receipt.txt"
    write_receipt(str(target), ["baris satu"])
    # read_text pakai universal newline: \r\n Windows normalisasi ke \n
    assert target.read_text(encoding="utf-8") == "baris satu\n"
    write_receipt(str(target), ["baru", "tulis ulang"])
    assert target.read_text(encoding="utf-8") == "baru\ntulis ulang\n"
