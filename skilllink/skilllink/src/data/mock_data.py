"""
Mock data layer for SkillLink.
Provides rich, realistic sample data for client & provider flows.
"""

SERVICES = [
    {"code": "R", "label": "Ride", "icon": "🚗", "desc": "Quick city rides"},
    {"code": "D", "label": "Delivery", "icon": "📦", "desc": "Parcel delivery"},
    {"code": "P", "label": "Plumber", "icon": "🔧", "desc": "Pipes & repairs"},
    {"code": "E", "label": "Electrician", "icon": "⚡", "desc": "Wiring & fixtures"},
    {"code": "AC", "label": "AC Repair", "icon": "❄️", "desc": "Cooling & gas"},
    {"code": "C", "label": "Cleaning", "icon": "🧹", "desc": "Home deep clean"},
]

PROVIDERS = [
    {
        "id": "p1",
        "name": "Ahmed Khan",
        "service": "Ride",
        "verified": True,
        "vehicle": "Toyota Corolla (ABC-123)",
        "trips": 142,
        "rating": 4.9,
        "eta": "3 min",
        "distance": "0.8 km",
        "price": 850,
        "phone": "+92 301 5551234",
        "lat_offset": 0.003,
        "lon_offset": 0.002,
        "badge": "Top Driver",
    },
    {
        "id": "p2",
        "name": "Usman Ali",
        "service": "Plumber",
        "verified": True,
        "vehicle": "Service Bike (XYZ-987)",
        "trips": 89,
        "rating": 4.8,
        "eta": "7 min",
        "distance": "1.4 km",
        "price": 650,
        "phone": "+92 321 8887766",
        "lat_offset": -0.004,
        "lon_offset": 0.003,
        "badge": "Certified Pro",
    },
    {
        "id": "p3",
        "name": "Bilal Tariq",
        "service": "Electrician",
        "verified": True,
        "vehicle": "Suzuki Alto (LEA-456)",
        "trips": 64,
        "rating": 4.7,
        "eta": "12 min",
        "distance": "2.1 km",
        "price": 900,
        "phone": "+92 333 4443322",
        "lat_offset": 0.005,
        "lon_offset": -0.004,
        "badge": "Fast Responder",
    },
    {
        "id": "p4",
        "name": "Hamza Farooq",
        "service": "Delivery",
        "verified": True,
        "vehicle": "Honda CD 70 (ICT-321)",
        "trips": 210,
        "rating": 4.9,
        "eta": "5 min",
        "distance": "1.1 km",
        "price": 350,
        "phone": "+92 345 9991122",
        "lat_offset": -0.002,
        "lon_offset": -0.003,
        "badge": "Express Courier",
    },
    {
        "id": "p5",
        "name": "Zeeshan Malik",
        "service": "AC Repair",
        "verified": True,
        "vehicle": "FAW Carrier (ISB-778)",
        "trips": 115,
        "rating": 4.9,
        "eta": "15 min",
        "distance": "3.0 km",
        "price": 1200,
        "phone": "+92 300 7776655",
        "lat_offset": 0.006,
        "lon_offset": 0.005,
        "badge": "HVAC Expert",
    },
]

OFFERS = [
    {
        "code": "FREEDEL",
        "title": "Free Delivery",
        "subtitle": "Get 100% off delivery fee on your next 3 orders",
        "discount": 350,
    },
    {
        "code": "SKILL20",
        "title": "20% Off Home Services",
        "subtitle": "Valid on Plumber and Electrician bookings",
        "discount": 200,
    },
    {
        "code": "CASH10",
        "title": "10% Wallet Cashback",
        "subtitle": "Add Rs. 1000+ to wallet and get Rs. 100 bonus",
        "discount": 100,
    },
]

INITIAL_BOOKINGS = [
    {
        "id": "BK-1082",
        "service": "Ride Service",
        "provider": "Ahmed Khan",
        "provider_phone": "+92 301 5551234",
        "date": "Today, 1:15 PM",
        "status": "In Progress",  # In Progress, Completed, Cancelled
        "step": 2,  # 0: Assigned, 1: En Route, 2: Arrived, 3: Completed
        "otp_pin": "4821",
        "pickup": "F-8 Markaz, Islamabad",
        "dropoff": "Blue Area, Islamabad",
        "fare": 850,
        "payment_method": "JazzCash",
    },
    {
        "id": "BK-1079",
        "service": "Plumber Service",
        "provider": "Usman Ali",
        "provider_phone": "+92 321 8887766",
        "date": "10 Apr 2026",
        "status": "Completed",
        "step": 3,
        "otp_pin": "9120",
        "pickup": "Street 14, F-8/3, Islamabad",
        "dropoff": "On-Site Repair",
        "fare": 650,
        "payment_method": "Cash on Delivery",
    },
]

INITIAL_INCOMING_REQUESTS = [
    {
        "id": "REQ-501",
        "client_name": "Sara Malik",
        "service": "Ride Service",
        "pickup": "F-7 Jinnah Super",
        "dropoff": "Centaurus Mall",
        "offered_fare": 650,
        "distance": "2.4 km",
        "time": "Just now",
    },
    {
        "id": "REQ-502",
        "client_name": "Omer Tariq",
        "service": "Delivery",
        "pickup": "G-9 Markaz",
        "dropoff": "F-10 Markaz",
        "offered_fare": 400,
        "distance": "3.8 km",
        "time": "2 min ago",
    },
]

INITIAL_NOTIFICATIONS = [
    {"id": "n1", "title": "Trip Booked", "text": "Ahmed Khan accepted your ride request.", "time": "5m ago", "read": False},
    {"id": "n2", "title": "Promo Unlocked", "text": "Use code SKILL20 for 20% off home repairs.", "time": "1h ago", "read": False},
    {"id": "n3", "title": "Payment Confirmed", "text": "Rs. 650 paid to Usman Ali via Cash.", "time": "2d ago", "read": True},
]

INITIAL_SAVED_LOCATIONS = [
    {"label": "Home", "address": "House 42, St 15, F-8/2, Islamabad", "icon": "🏠"},
    {"label": "Office", "address": "Evacuee Trust Complex, F-5/1, Islamabad", "icon": "💼"},
    {"label": "Gym", "address": "Fitness First, Beverly Centre, Blue Area", "icon": "🏋️"},
]

CHAT_MESSAGES = {
    "Ahmed Khan": [
        {"role": "them", "text": "Assalam-o-Alaikum! I have arrived outside your pickup gate.", "time": "1:16 PM"},
        {"role": "me", "text": "Walaikum Assalam, I'm coming down in 1 minute.", "time": "1:17 PM"},
    ],
    "Usman Ali": [
        {"role": "them", "text": "I have completed the plumbing fixture work.", "time": "Apr 10"},
        {"role": "me", "text": "Thank you! Everything works perfectly.", "time": "Apr 10"},
    ],
}
