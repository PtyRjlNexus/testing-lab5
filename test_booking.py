import pytest
from unittest.mock import Mock
from datetime import date
from booking_service import BookingService, BookingRequest

def test_create_booking_success():
    # ARRANGE (Підготовка)
    mock_db = Mock()
    mock_email = Mock()
    mock_db.is_room_available.return_value = True
    mock_db.save_booking.return_value = 101

    service = BookingService(repository=mock_db, email_service=mock_email)
    request = BookingRequest(
        user_email="student@univ.edu.ua",
        room_id=12,
        start_date=date(2026, 11, 1),
        end_date=date(2026, 11, 5),
        price_per_night=150.0
    )

    # ACT (Дія)
    response = service.create_booking(request)

    # ASSERT (Перевірка)
    assert response.booking_id == 101
    assert response.status == "CONFIRMED"
    assert response.total_price == 600.0
    mock_db.is_room_available.assert_called_once()
    mock_email.send_confirmation.assert_called_once()