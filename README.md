# 🔗 SkillLink — On-Demand Services & Mobility Platform

A sleek, mobile-first frontend prototype for an on-demand service and ride booking ecosystem built in Streamlit (Python).

---

## 🚀 Key Features

### 👤 Client App
- **2-Step OTP Authentication**: Phone login with Pakistani format (+92) and demo code (`1234`).
- **Live GPS Radar & Proximity Map**: Interactive Leaflet map powered by `folium` and `streamlit-folium` with OpenStreetMap tiles (no API keys required), live nearby provider pins with rich popup badges, 5-minute coverage radius, and free address geocoding via the public OpenStreetMap Nominatim endpoint.
- **On-Demand Categories**: Instant booking for Rides, Delivery, Plumbing, Electrician, AC Repair, and Cleaning.
- **Real-Time Fare Negotiation**: Bid custom fares against provider asking prices with realistic simulated acceptance.
- **Full Booking & Checkout**: Pickup/Dropoff selection, promo code discounts, and JazzCash/EasyPaisa/Wallet payment options.
- **Active Trip Lifecycle Tracker**: Real-time progress bar (*Assigned ➔ En Route ➔ Arrived ➔ Completed*) with driver verification PIN.
- **Smart Chat & Quick Replies**: Auto-replying provider messaging and simulated calling.
- **Profile & Wallet**: Saved locations manager, wallet top-up, and 24/7 safety helpline.

### 🚗 Provider App
- **Availability Switch**: Instant Online / Offline toggle with pulsating indicator.
- **Live Dispatch Queue**: Incoming ride/service requests with Accept and Decline actions.
- **Active Job Fulfillment**: Step-by-step order tracking with payout collection upon completion.
- **Earnings Dashboard**: Today's revenue, completed trips, and acceptance ratings.

---

## 🛠️ How to Run in Visual Studio Code

### 1. Open the project folder in VS Code
Open the root directory where `app.py` is located:
```bash
c:\Users\lifeo\Downloads\skilllink\skilllink\skilllink
```

### 2. Open the Terminal in VS Code
Press `Ctrl + ` ` ` (backtick) or go to **Terminal > New Terminal**.

### 3. Create / Activate Virtual Environment (Optional but recommended)
```powershell
# In PowerShell:
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Launch the Streamlit App
```powershell
streamlit run app.py
```

The app will open in your browser automatically at `http://localhost:8501`.
