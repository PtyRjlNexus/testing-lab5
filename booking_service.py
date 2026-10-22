from dataclasses import dataclass
from datetime import date

@dataclass
class BookingRequest:
    user_email: str
    room_id: int
    start_date: date
    end_date: date
    price_per_night: float

@dataclass
class BookingResponse:
    booking_id: int
    status: str
    total_price: float

class BookingService:
    def __init__(self, repository, email_service):
        self.repository = repository
        self.email_service = email_service

    def create_booking(self, request: BookingRequest) -> BookingResponse:
        if request.end_date <= request.start_date:
            raise ValueError("Некоректні дати бронювання")

        if not self.repository.is_room_available(request.room_id, request.start_date, request.end_date):
            raise ValueError("Номер зайнятий на ці дати")

        nights = (request.end_date - request.start_date).days
        total_price = nights * request.price_per_night

        booking_id = self.repository.save_booking(
            room_id=request.room_id,
            user_email=request.user_email,
            start_date=request.start_date,
            end_date=request.end_date,
            total_price=total_price
        )

        self.email_service.send_confirmation(request.user_email, booking_id, total_price)

        return BookingResponse(booking_id=booking_id, status="CONFIRMED", total_price=total_price)