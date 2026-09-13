/**
 * SkillLink Web Application Engine
 * Pure client-side reactive state machine for 60fps smooth mobile interactions.
 */

const STATE = {
  mode: 'Client', // 'Client' or 'Partner'
  currentView: 'auth', // 'auth', 'home', 'providers', 'bookings', 'chat', 'profile', 'partner'
  isAuthenticated: false,
  userLocation: 'F-8 Markaz, Islamabad',
  walletBalance: 1850,
  activeFilter: 'All',
  searchQuery: '',
  appliedPromo: null,
  discountAmount: 0,
  selectedProvider: null,
  activeChatPartner: 'Ahmed Khan',
  partnerOnline: true,
  partnerEarnings: 2400,
  partnerJobs: 3,
  partnerActiveJob: null,

  providers: [
    { id: 'p1', name: 'Ahmed Khan', service: 'Ride', verified: true, vehicle: 'Toyota Corolla (ABC-123)', trips: 142, rating: 4.9, eta: '3 min', distance: '0.8 km', price: 850, badge: 'Top Driver', phone: '+92 301 5551234' },
    { id: 'p2', name: 'Usman Ali', service: 'Plumber', verified: true, vehicle: 'Service Bike (XYZ-987)', trips: 89, rating: 4.8, eta: '7 min', distance: '1.4 km', price: 650, badge: 'Certified Pro', phone: '+92 321 8887766' },
    { id: 'p3', name: 'Bilal Tariq', service: 'Electrician', verified: true, vehicle: 'Suzuki Alto (LEA-456)', trips: 64, rating: 4.7, eta: '12 min', distance: '2.1 km', price: 900, badge: 'Fast Responder', phone: '+92 333 4443322' },
    { id: 'p4', name: 'Hamza Farooq', service: 'Delivery', verified: true, vehicle: 'Honda CD 70 (ICT-321)', trips: 210, rating: 4.9, eta: '5 min', distance: '1.1 km', price: 350, badge: 'Express Courier', phone: '+92 345 9991122' },
    { id: 'p5', name: 'Zeeshan Malik', service: 'AC Repair', verified: true, vehicle: 'FAW Carrier (ISB-778)', trips: 115, rating: 4.9, eta: '15 min', distance: '3.0 km', price: 1200, badge: 'HVAC Expert', phone: '+92 300 7776655' }
  ],

  bookings: [
    { id: 'BK-1082', service: 'Ride Service', provider: 'Ahmed Khan', providerPhone: '+92 301 5551234', date: 'Today, 1:15 PM', status: 'In Progress', step: 2, pin: '4821', fare: 850, pickup: 'F-8 Markaz, Islamabad', dropoff: 'Blue Area, Islamabad', payment: 'JazzCash' },
    { id: 'BK-1079', service: 'Plumber Service', provider: 'Usman Ali', providerPhone: '+92 321 8887766', date: '10 Apr 2026', status: 'Completed', step: 3, pin: '9120', fare: 650, pickup: 'Street 14, F-8/3', dropoff: 'On-Site Repair', payment: 'Cash' }
  ],

  notifications: [
    { id: 'n1', title: 'Trip Booked', text: 'Ahmed Khan accepted your ride request.', time: '5m ago', read: false },
    { id: 'n2', title: 'Promo Unlocked', text: 'Use code SKILL20 for 20% off home repairs.', time: '1h ago', read: false },
    { id: 'n3', title: 'Payment Confirmed', text: 'Rs. 650 paid to Usman Ali via Cash.', time: '2d ago', read: true }
  ],

  incomingRequests: [
    { id: 'REQ-501', clientName: 'Sara Malik', service: 'Ride Service', pickup: 'F-7 Jinnah Super', dropoff: 'Centaurus Mall', fare: 650, distance: '2.4 km', time: 'Just now' },
    { id: 'REQ-502', clientName: 'Omer Tariq', service: 'Delivery', pickup: 'G-9 Markaz', dropoff: 'F-10 Markaz', fare: 400, distance: '3.8 km', time: '2 min ago' }
  ],

  chatMessages: {
    'Ahmed Khan': [
      { role: 'them', text: 'Assalam-o-Alaikum! I have arrived outside your pickup gate.', time: '1:16 PM' },
      { role: 'me', text: 'Walaikum Assalam, I am coming down in 1 minute.', time: '1:17 PM' }
    ],
    'Usman Ali': [
      { role: 'them', text: 'I have completed the plumbing fixture work.', time: 'Apr 10' },
      { role: 'me', text: 'Thank you! Everything works perfectly.', time: 'Apr 10' }
    ]
  }
};

// ---------- INITIALIZATION ----------
window.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) lucide.createIcons();
  renderAll();
});

function renderAll() {
  renderActiveTripBanner();
  renderNotifications();
  renderFilterChips();
  renderProviders();
  renderBookings();
  renderChat();
  renderPartnerView();
  if (window.lucide) lucide.createIcons();
}

// ---------- NAVIGATION & ROUTING ----------
function navigateTo(viewName) {
  STATE.currentView = viewName;

  // Hide all screens
  document.querySelectorAll('.view-screen').forEach(el => el.classList.remove('active'));
  
  // Show target
  const target = document.getElementById(`view-${viewName}`);
  if (target) target.classList.add('active');

  // Update Bottom Nav
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const navMap = {
    home: 'navHome',
    bookings: 'navBookings',
    chat: 'navChat',
    profile: 'navProfile'
  };
  if (navMap[viewName]) {
    const navBtn = document.getElementById(navMap[viewName]);
    if (navBtn) navBtn.classList.add('active');
  }

  // Hide bottom nav in auth view or partner view
  const bottomNav = document.getElementById('mainBottomNav');
  if (viewName === 'auth' || STATE.mode === 'Partner') {
    bottomNav.classList.add('hidden');
  } else {
    bottomNav.classList.remove('hidden');
  }

  renderAll();
}

function switchMode(newMode) {
  STATE.mode = newMode;
  document.getElementById('btnModeClient').classList.toggle('active', newMode === 'Client');
  document.getElementById('btnModePartner').classList.toggle('active', newMode === 'Partner');

  if (newMode === 'Partner') {
    navigateTo('partner');
  } else {
    navigateTo('home');
  }
}

// ---------- AUTH LOGIC ----------
function requestOTP() {
  const phone = document.getElementById('inputAuthPhone').value;
  if (phone.trim().length >= 10) {
    document.getElementById('displayOtpPhone').innerText = phone;
    document.getElementById('authStepPhone').classList.add('hidden');
    document.getElementById('authStepOTP').classList.remove('hidden');
    showToast('OTP Sent! Demo code: 1234');
  } else {
    showToast('Please enter a valid mobile number');
  }
}

function verifyOTP() {
  const code = document.getElementById('inputAuthOTP').value;
  if (code === '1234' || code.length === 4) {
    STATE.isAuthenticated = true;
    showToast('Verification Successful! Welcome to SkillLink.');
    navigateTo('home');
  } else {
    showToast('Invalid Code. Please enter 1234');
  }
}

function instantDemoLogin() {
  STATE.isAuthenticated = true;
  showToast('Logged in as Abeer Ahmed (Demo Mode)');
  navigateTo('home');
}

function backToPhoneStep() {
  document.getElementById('authStepOTP').classList.add('hidden');
  document.getElementById('authStepPhone').classList.remove('hidden');
}

function logout() {
  STATE.isAuthenticated = false;
  navigateTo('auth');
  backToPhoneStep();
  showToast('Logged out successfully.');
}

// ---------- TOAST NOTIFICATION ENGINE ----------
function showToast(message) {
  const box = document.getElementById('toastBox');
  const toast = document.createElement('div');
  toast.className = 'toast-msg';
  toast.innerText = message;
  box.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    setTimeout(() => toast.remove(), 300);
  }, 2600);
}

// ---------- NOTIFICATIONS DRAWER ----------
function toggleNotifs() {
  const drawer = document.getElementById('drawerNotifs');
  drawer.classList.toggle('hidden');
}

function renderNotifications() {
  const list = document.getElementById('notifList');
  if (!list) return;
  list.innerHTML = STATE.notifications.map(n => `
    <div class="bg-slate-900/90 border-l-2 border-blue-500 p-2 rounded-xl">
      <div class="flex justify-between font-bold text-white">
        <span>${n.title}</span><span class="text-[10px] text-slate-400">${n.time}</span>
      </div>
      <p class="text-[11px] text-slate-300 mt-0.5">${n.text}</p>
    </div>
  `).join('');
}

// ---------- HOME & CATEGORIES ----------
function selectService(srvName) {
  STATE.activeFilter = srvName;
  STATE.searchQuery = '';
  document.getElementById('providersHeaderTitle').innerText = srvName === 'All' ? 'Available Providers' : `${srvName} Specialists`;
  navigateTo('providers');
}

function handleSearch(query) {
  STATE.searchQuery = query;
  if (query.trim().length > 0 && STATE.currentView !== 'providers') {
    STATE.activeFilter = 'All';
    navigateTo('providers');
  } else {
    renderProviders();
  }
}

function applyPromo(code, discount) {
  STATE.appliedPromo = code;
  STATE.discountAmount = discount;
  showToast(`Promo ${code} applied! Saved Rs. ${discount}.`);
}

function renderActiveTripBanner() {
  const banner = document.getElementById('bannerActiveTrip');
  const activeJob = STATE.bookings.find(b => b.status === 'In Progress');
  if (activeJob) {
    banner.classList.remove('hidden');
    document.getElementById('activeTripTitle').innerText = activeJob.service;
    document.getElementById('activeTripSubtitle').innerHTML = `Driver: <b>${activeJob.provider}</b>`;
    document.getElementById('activeTripPIN').innerText = activeJob.pin;
  } else {
    banner.classList.add('hidden');
  }
}

// ---------- PROVIDERS SCREEN ----------
function renderFilterChips() {
  const chipsBox = document.getElementById('providerFilterChips');
  if (!chipsBox) return;
  const categories = ['All', 'Ride', 'Delivery', 'Plumber', 'Electrician', 'AC Repair', 'Cleaning'];
  chipsBox.innerHTML = categories.map(cat => `
    <button class="px-3.5 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${STATE.activeFilter === cat ? 'bg-blue-600 text-white shadow-md shadow-blue-500/30' : 'bg-slate-900 border border-white/10 text-slate-400 hover:border-slate-600'}" onclick="setCategoryFilter('${cat}')">
      ${cat}
    </button>
  `).join('');
}

function setCategoryFilter(cat) {
  STATE.activeFilter = cat;
  renderFilterChips();
  renderProviders();
}

function renderProviders() {
  const container = document.getElementById('providersListContainer');
  if (!container) return;

  let list = STATE.providers.filter(p => {
    if (STATE.activeFilter !== 'All' && p.service !== STATE.activeFilter) return false;
    if (STATE.searchQuery.trim()) {
      const q = STATE.searchQuery.toLowerCase();
      return p.name.toLowerCase().includes(q) || p.service.toLowerCase().includes(q) || p.vehicle.toLowerCase().includes(q);
    }
    return true;
  });

  if (list.length === 0) {
    container.innerHTML = `<div class="card text-center text-xs text-slate-400 py-8">No providers found for this category.</div>`;
    return;
  }

  container.innerHTML = list.map(p => `
    <div class="card">
      <div class="flex justify-between items-start">
        <div>
          <div class="flex items-center gap-1.5">
            <b class="text-sm text-white">${p.name}</b>
            <span class="text-sky-400 text-xs">✅</span>
            <span class="badge-tag text-[9px] py-0.5 px-1.5">${p.badge}</span>
          </div>
          <span class="text-xs text-slate-400">${p.service} • ${p.vehicle}</span>
          <div class="mt-1 flex items-center gap-2 text-xs">
            <span class="text-amber-400 font-bold">★ ${p.rating}</span>
            <span class="text-slate-500">(${p.trips} jobs)</span>
          </div>
        </div>
        <div class="text-right">
          <b class="text-base font-extrabold text-blue-400">Rs. ${p.price}</b><br>
          <span class="text-emerald-400 text-[11px] font-bold">📍 ${p.distance} • ${p.eta}</span>
        </div>
      </div>
      <div class="grid grid-cols-2 gap-2 mt-3 pt-2.5 border-t border-white/10">
        <button class="btn-secondary !py-2 text-xs" onclick="openNegotiation('${p.id}')">🤝 Negotiate</button>
        <button class="btn-primary !py-2 text-xs" onclick="openCheckout('${p.id}')">⚡ Book Now</button>
      </div>
    </div>
  `).join('');
}

// ---------- NEGOTIATION & CHECKOUT MODALS ----------
function openNegotiation(providerId) {
  const p = STATE.providers.find(item => item.id === providerId);
  STATE.selectedProvider = p;
  document.getElementById('negProviderDetails').innerHTML = `Provider: <b>${p.name}</b> (${p.service}) • Asking Fare: <b>Rs. ${p.price}</b>`;
  document.getElementById('inputCounterBid').value = Math.max(100, p.price - 150);
  openModal('modalNegotiation');
}

function submitCounterBid() {
  const p = STATE.selectedProvider;
  const bid = parseInt(document.getElementById('inputCounterBid').value);
  closeModal('modalNegotiation');

  const ratio = bid / p.price;
  if (ratio >= 0.8) {
    showToast(`🎉 ${p.name} ACCEPTED your offer of Rs. ${bid}!`);
    const newBooking = {
      id: `BK-${Math.floor(1000 + Math.random() * 9000)}`,
      service: `${p.service} Service`,
      provider: p.name,
      providerPhone: p.phone,
      date: 'Just now',
      status: 'In Progress',
      step: 0,
      pin: `${Math.floor(1000 + Math.random() * 9000)}`,
      fare: bid,
      pickup: STATE.userLocation,
      dropoff: 'Destination Location',
      payment: 'Cash on Delivery'
    };
    STATE.bookings.unshift(newBooking);
    STATE.activeChatPartner = p.name;
    navigateTo('bookings');
  } else {
    const counter = Math.round(p.price * 0.9);
    showToast(`⚠️ ${p.name} countered with Rs. ${counter}.`);
  }
}

function openCheckout(providerId) {
  const p = STATE.providers.find(item => item.id === providerId);
  STATE.selectedProvider = p;
  const discount = STATE.discountAmount || 0;
  const finalFare = Math.max(50, p.price - discount);

  document.getElementById('checkoutSummaryBox').innerHTML = `
    <div class="flex justify-between items-center text-xs">
      <div>
        <b class="text-white">${p.name}</b> • <span class="text-slate-400">${p.service}</span><br>
        <span class="text-slate-400">${p.vehicle}</span>
      </div>
      <div class="text-right">
        <b class="text-blue-400 font-bold text-sm">Rs. ${finalFare}</b><br>
        ${discount > 0 ? `<span class="text-emerald-400 text-[10px]">Saved Rs. ${discount}</span>` : ''}
      </div>
    </div>
  `;
  openModal('modalCheckout');
}

function confirmOrder() {
  const p = STATE.selectedProvider;
  const payment = document.getElementById('selectPaymentMethod').value.split(' ')[0];
  const discount = STATE.discountAmount || 0;
  const finalFare = Math.max(50, p.price - discount);

  closeModal('modalCheckout');
  showToast(`Order confirmed with ${p.name}!`);

  const newBooking = {
    id: `BK-${Math.floor(2000 + Math.random() * 8000)}`,
    service: `${p.service} Service`,
    provider: p.name,
    providerPhone: p.phone,
    date: 'Just now',
    status: 'In Progress',
    step: 0,
    pin: `${Math.floor(1000 + Math.random() * 9000)}`,
    fare: finalFare,
    pickup: STATE.userLocation,
    dropoff: 'Destination Location',
    payment: payment
  };
  STATE.bookings.unshift(newBooking);
  STATE.activeChatPartner = p.name;
  navigateTo('bookings');
}

function openModal(id) {
  const modal = document.getElementById(id);
  modal.classList.add('open');
}

function closeModal(id) {
  const modal = document.getElementById(id);
  modal.classList.remove('open');
}

// ---------- BOOKINGS & TRACKER ----------
const ORDER_STEPS = ['Assigned', 'En Route', 'Arrived', 'Completed'];

function switchBookingTab(tab) {
  const activeTabBtn = document.getElementById('tabBookActive');
  const histTabBtn = document.getElementById('tabBookHistory');
  const activePanel = document.getElementById('panelBookActive');
  const histPanel = document.getElementById('panelBookHistory');

  if (tab === 'active') {
    activeTabBtn.className = 'flex-1 py-1.5 text-xs font-bold text-blue-400 bg-slate-800 rounded-xl shadow';
    histTabBtn.className = 'flex-1 py-1.5 text-xs font-bold text-slate-400';
    activePanel.classList.remove('hidden');
    histPanel.classList.add('hidden');
  } else {
    histTabBtn.className = 'flex-1 py-1.5 text-xs font-bold text-blue-400 bg-slate-800 rounded-xl shadow';
    activeTabBtn.className = 'flex-1 py-1.5 text-xs font-bold text-slate-400';
    histPanel.classList.remove('hidden');
    activePanel.classList.add('hidden');
  }
}

function renderBookings() {
  const activePanel = document.getElementById('panelBookActive');
  const histPanel = document.getElementById('panelBookHistory');
  if (!activePanel || !histPanel) return;

  const active = STATE.bookings.find(b => b.status === 'In Progress');
  if (!active) {
    activePanel.innerHTML = `
      <div class="card text-center py-8">
        <div class="text-3xl mb-2">🚗</div>
        <b class="text-sm text-white">No Active Orders</b>
        <p class="text-xs text-slate-400 mt-1 mb-3">You do not have any ongoing rides or services.</p>
        <button class="btn-primary text-xs mx-auto max-w-[200px]" onclick="navigateTo('home')">Browse Services ➔</button>
      </div>
    `;
  } else {
    const sIdx = active.step || 0;
    activePanel.innerHTML = `
      <div class="card-highlight">
        <div class="flex justify-between items-start">
          <div>
            <span class="badge-active"><span class="pulse-dot"></span> Status: ${ORDER_STEPS[sIdx]}</span>
            <h3 class="font-extrabold text-base text-white mt-1.5">${active.service}</h3>
            <span class="text-xs text-slate-400">Order ID: ${active.id}</span>
          </div>
          <div class="text-right">
            <span class="text-[10px] text-slate-400 font-bold">DRIVER PIN</span>
            <div class="text-xs font-extrabold bg-emerald-600 text-white px-2 py-0.5 rounded-lg mt-0.5">${active.pin}</div>
          </div>
        </div>

        <!-- Progress Stepper -->
        <div class="mt-3.5 bg-slate-800 rounded-full h-2 overflow-hidden">
          <div class="bg-gradient-to-r from-blue-500 to-emerald-400 h-full transition-all duration-300" style="width: ${(sIdx + 1) * 25}%"></div>
        </div>
        <div class="flex justify-between text-[10px] font-bold text-slate-400 mt-1">
          <span class="${sIdx >= 0 ? 'text-blue-400' : ''}">Assigned</span>
          <span class="${sIdx >= 1 ? 'text-blue-400' : ''}">En Route</span>
          <span class="${sIdx >= 2 ? 'text-blue-400' : ''}">Arrived</span>
          <span class="${sIdx >= 3 ? 'text-emerald-400' : ''}">Done</span>
        </div>
      </div>

      <div class="card">
        <div class="flex justify-between items-center">
          <div>
            <b class="text-sm text-white">${active.provider}</b><br>
            <span class="text-xs text-slate-400">📞 ${active.providerPhone}</span>
          </div>
          <div class="text-right">
            <b class="text-base text-blue-400 font-extrabold">Rs. ${active.fare}</b><br>
            <span class="text-[11px] text-slate-400">${active.payment}</span>
          </div>
        </div>
        <div class="mt-2.5 pt-2 border-t border-white/10 text-xs text-slate-300">
          📍 <b>Pickup:</b> ${active.pickup}<br>
          🎯 <b>Dropoff:</b> ${active.dropoff}
        </div>
        <div class="grid grid-cols-3 gap-2 mt-3">
          <button class="btn-primary !py-2 text-xs" onclick="openChatWith('${active.provider}')">💬 Chat</button>
          <button class="btn-secondary !py-2 text-xs" onclick="showToast('Calling ${active.provider}...')">📞 Call</button>
          <button class="btn-secondary !py-2 text-xs !text-rose-400" onclick="cancelActiveOrder('${active.id}')">Cancel</button>
        </div>
      </div>

      ${sIdx < 3 ? `
        <button class="btn-secondary !py-2 text-xs mt-2 text-blue-400" onclick="advanceOrderStage('${active.id}')">
          ⚡ Demo: Advance Stage (${ORDER_STEPS[sIdx + 1]}) ➔
        </button>
      ` : ''}
    `;
  }

  // Render History
  const history = STATE.bookings.filter(b => b.status !== 'In Progress');
  histPanel.innerHTML = history.map(b => `
    <div class="card !p-3">
      <div class="flex justify-between items-center">
        <b class="text-xs text-white">${b.service}</b>
        <span class="${b.status === 'Completed' ? 'badge-completed' : 'badge-pending'}">${b.status}</span>
      </div>
      <span class="text-[11px] text-slate-400">Provider: ${b.provider} • ${b.date}</span>
      <div class="flex justify-between items-center mt-2 pt-2 border-t border-white/10">
        <span class="text-xs text-slate-400">Paid Fare</span>
        <b class="text-xs text-blue-400">Rs. ${b.fare}</b>
      </div>
    </div>
  `).join('');
}

function advanceOrderStage(orderId) {
  const b = STATE.bookings.find(item => item.id === orderId);
  if (b && b.step < 3) {
    b.step += 1;
    if (b.step === 3) {
      b.status = 'Completed';
      showToast('🎉 Order completed successfully!');
    }
    renderBookings();
    renderActiveTripBanner();
  }
}

function cancelActiveOrder(orderId) {
  const b = STATE.bookings.find(item => item.id === orderId);
  if (b) {
    b.status = 'Cancelled';
    showToast('Order cancelled.');
    renderBookings();
    renderActiveTripBanner();
  }
}

// ---------- CHAT SCREEN ----------
function openChatWith(providerName) {
  STATE.activeChatPartner = providerName;
  navigateTo('chat');
}

function renderChat() {
  const box = document.getElementById('chatMessagesBox');
  if (!box) return;
  document.getElementById('chatProviderName').innerText = STATE.activeChatPartner;

  if (!STATE.chatMessages[STATE.activeChatPartner]) {
    STATE.chatMessages[STATE.activeChatPartner] = [
      { role: 'them', text: `Assalam-o-Alaikum! I am your SkillLink specialist for today.`, time: 'Just now' }
    ];
  }

  box.innerHTML = STATE.chatMessages[STATE.activeChatPartner].map(m => `
    <div class="flex ${m.role === 'me' ? 'justify-end' : 'justify-start'}">
      <div class="${m.role === 'me' ? 'bg-blue-600 text-white rounded-2xl rounded-tr-sm' : 'bg-slate-800 text-slate-200 rounded-2xl rounded-tl-sm'} p-3 max-w-[80%] text-xs shadow">
        <p>${m.text}</p>
        <span class="block text-[9px] ${m.role === 'me' ? 'text-blue-200' : 'text-slate-400'} text-right mt-1">${m.time}</span>
      </div>
    </div>
  `).join('');
}

function submitChatMsg() {
  const input = document.getElementById('inputChatMsg');
  const val = input.value.trim();
  if (val) {
    sendChatMsg(val);
    input.value = '';
  }
}

function sendChatMsg(text) {
  const partner = STATE.activeChatPartner;
  if (!STATE.chatMessages[partner]) STATE.chatMessages[partner] = [];
  
  STATE.chatMessages[partner].push({
    role: 'me',
    text: text,
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  });
  renderChat();

  // Automated simulated reply
  setTimeout(() => {
    const replies = [
      "Understood, I am 2 minutes away!",
      "Got it, arriving at your location shortly.",
      "Sure, no problem at all!",
      "Thanks for confirming, see you soon."
    ];
    const reply = replies[Math.floor(Math.random() * replies.length)];
    STATE.chatMessages[partner].push({
      role: 'them',
      text: reply,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
    renderChat();
  }, 1000);
}

// ---------- PROFILE & WALLET ----------
function topUpWallet(amount) {
  STATE.walletBalance += amount;
  document.getElementById('lblWalletBalance').innerText = `Rs. ${STATE.walletBalance.toLocaleString()}`;
  showToast(`Top-up successful: + Rs. ${amount}`);
}

// ---------- PARTNER / PROVIDER MODE ----------
function togglePartnerOnline() {
  STATE.partnerOnline = !STATE.partnerOnline;
  renderPartnerView();
  showToast(`Partner status: ${STATE.partnerOnline ? 'ONLINE' : 'OFFLINE'}`);
}

function renderPartnerView() {
  const statusBtn = document.getElementById('btnPartnerStatus');
  const queue = document.getElementById('partnerQueueContainer');
  const activeJobBox = document.getElementById('partnerActiveJobCard');
  if (!statusBtn || !queue) return;

  if (STATE.partnerOnline) {
    statusBtn.className = 'px-3 py-1.5 rounded-xl text-xs font-bold border border-emerald-500/40 bg-emerald-950/30 text-emerald-400 flex items-center gap-1.5';
    statusBtn.innerHTML = `<span class="pulse-dot"></span> ONLINE`;
  } else {
    statusBtn.className = 'px-3 py-1.5 rounded-xl text-xs font-bold border border-slate-700 bg-slate-900 text-slate-400';
    statusBtn.innerHTML = `⚫ OFFLINE`;
  }

  document.getElementById('lblPartnerEarnings').innerText = `Rs. ${STATE.partnerEarnings.toLocaleString()}`;
  document.getElementById('lblPartnerJobs').innerText = STATE.partnerJobs;

  // Active Job in Provider Mode
  if (STATE.partnerActiveJob) {
    activeJobBox.classList.remove('hidden');
    const job = STATE.partnerActiveJob;
    activeJobBox.innerHTML = `
      <div class="flex justify-between items-start">
        <div>
          <span class="badge-active"><span class="pulse-dot"></span> Active Job Execution</span>
          <h4 class="font-bold text-sm text-white mt-1">${job.service}</h4>
          <span class="text-xs text-slate-400">Client: <b>${job.clientName}</b> (${job.distance})</span>
        </div>
        <div class="text-right">
          <b class="text-blue-400 text-base">Rs. ${job.fare}</b><br>
          <span class="text-emerald-400 text-[10px]">Payment: Cash</span>
        </div>
      </div>
      <div class="mt-2 text-xs text-slate-300">
        📍 <b>Pickup:</b> ${job.pickup}<br>
        🎯 <b>Dropoff:</b> ${job.dropoff}
      </div>
      <div class="grid grid-cols-2 gap-2 mt-3">
        <button class="btn-secondary !py-2 text-xs" onclick="showToast('Calling ${job.clientName}...')">📞 Call Client</button>
        <button class="btn-primary !py-2 text-xs" onclick="completePartnerJob()">Complete & Collect ✅</button>
      </div>
    `;
  } else {
    activeJobBox.classList.add('hidden');
  }

  // Incoming Requests Queue
  if (!STATE.partnerOnline) {
    queue.innerHTML = `<div class="card text-center text-xs text-slate-400 py-6">You are currently offline. Turn online to receive requests.</div>`;
    return;
  }

  if (STATE.incomingRequests.length === 0) {
    queue.innerHTML = `<div class="card text-center text-xs text-slate-400 py-6"><span class="pulse-dot"></span> Listening for nearby requests in Islamabad...</div>`;
    return;
  }

  queue.innerHTML = STATE.incomingRequests.map((req, idx) => `
    <div class="card">
      <div class="flex justify-between items-start">
        <div>
          <span class="badge-pending">Incoming Request • ${req.time}</span>
          <h4 class="font-bold text-sm text-white mt-1">${req.service}</h4>
          <span class="text-xs text-slate-400">Client: <b>${req.clientName}</b> (${req.distance})</span>
        </div>
        <div class="text-right">
          <b class="text-blue-400 font-extrabold text-base">Rs. ${req.fare}</b><br>
          <span class="text-emerald-400 text-[10px] font-bold">Offered Fare</span>
        </div>
      </div>
      <div class="mt-2 bg-slate-950 p-2 rounded-xl text-[11px] text-slate-400">
        📍 ${req.pickup} ➔ 🎯 ${req.dropoff}
      </div>
      <div class="grid grid-cols-2 gap-2 mt-3">
        <button class="btn-primary !py-2 text-xs" onclick="acceptIncomingJob(${idx})">Accept (Rs. ${req.fare}) ➔</button>
        <button class="btn-secondary !py-2 text-xs" onclick="declineIncomingJob(${idx})">Decline</button>
      </div>
    </div>
  `).join('');
}

function acceptIncomingJob(idx) {
  const job = STATE.incomingRequests[idx];
  STATE.partnerActiveJob = job;
  STATE.incomingRequests.splice(idx, 1);
  showToast(`Accepted request from ${job.clientName}!`);
  renderPartnerView();
}

function declineIncomingJob(idx) {
  STATE.incomingRequests.splice(idx, 1);
  showToast('Request declined.');
  renderPartnerView();
}

function completePartnerJob() {
  const fare = STATE.partnerActiveJob.fare;
  STATE.partnerEarnings += fare;
  STATE.partnerJobs += 1;
  STATE.partnerActiveJob = null;
  showToast(`🎉 Job completed! Rs. ${fare} added to earnings.`);
  renderPartnerView();
}
