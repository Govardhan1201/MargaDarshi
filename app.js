/* ═══════════════════════════════════════════════════════════════════════════
   MārgaDarshi – app.js
   Full interactivity: Route Finder, Chatbot, Map, Language Switcher, etc.
   ═══════════════════════════════════════════════════════════════════════════ */

'use strict';

// ─── State ────────────────────────────────────────────────────────────────
let currentLang = 'en';
let mapInstance = null;
let isLoggedIn = false;
let isRecording = false;
let recognition = null;
const demoUser = { name: 'Traveller', email: '' };

// ─── DOM Ready ────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initLanguageSwitcher();
    populateStopDropdowns();
    initRouteFinder();
    initTouristFinder();
    initTimetable();
    initMap();
    initChatbot();
    initCommunitySection();
    initFAQ();
    initScrollAnimations();
    initScrollSpy();
    showWelcomeChatMessage();

    // ── Visual Effects ──────────────────────────────────────────────────────
    initPageLoader();
    initCursor();
    initParallax();
    initTiltCards();
    initRippleButtons();
    initButtonSpotlight();
    initStatCountUp();
});

// ─── Helpers ──────────────────────────────────────────────────────────────
function t(key) {
    const translations = VIZAG_DATA.translations;
    return (translations[currentLang] && translations[currentLang][key])
        ? translations[currentLang][key]
        : (translations.en[key] || key);
}

function formatTime(now = new Date()) {
    return now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true });
}

function getCurrentCrowd() {
    const hour = new Date().getHours();
    return VIZAG_DATA.crowdByHour[hour] || 'medium';
}

function crowdClass(level) {
    const map = { 'empty': 'crowd-low', 'low': 'crowd-low', 'medium': 'crowd-medium', 'high': 'crowd-high', 'very high': 'crowd-very-high' };
    return map[level] || 'crowd-medium';
}

function crowdEmoji(level) {
    const map = { 'empty': '🟢', 'low': '🟢', 'medium': '🟡', 'high': '🔴', 'very high': '🔴' };
    return map[level] || '🟡';
}

function getStopName(id) {
    const stop = VIZAG_DATA.stops.find(s => s.id === id);
    return stop ? stop.name : id;
}

// ─── Navbar ───────────────────────────────────────────────────────────────
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');

    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });

    hamburger?.addEventListener('click', () => {
        mobileMenu.classList.toggle('open');
        const isOpen = mobileMenu.classList.contains('open');
        hamburger.setAttribute('aria-expanded', isOpen);
        hamburger.querySelectorAll('span')[0].style.transform = isOpen ? 'rotate(45deg) translate(5px, 5px)' : '';
        hamburger.querySelectorAll('span')[1].style.opacity = isOpen ? '0' : '1';
        hamburger.querySelectorAll('span')[2].style.transform = isOpen ? 'rotate(-45deg) translate(5px, -5px)' : '';
    });

    // Close mobile menu on link click
    mobileMenu?.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('open');
            hamburger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = '1'; });
        });
    });
}

// ─── Language Switcher ────────────────────────────────────────────────────
function initLanguageSwitcher() {
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            setLanguage(lang);
        });
    });
}

function setLanguage(lang) {
    if (!VIZAG_DATA.translations[lang]) return;
    currentLang = lang;

    // Update active button
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    // Update all data-i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        const text = t(key);
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = text;
        } else {
            el.textContent = text;
        }
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        el.setAttribute('placeholder', t(el.dataset.i18nPlaceholder));
    });

    // Repopulate dropdowns with current language stop names
    populateStopDropdowns();
    // Update timetable disclaimer
    const disc = document.getElementById('timetableDisclaimer');
    if (disc) disc.textContent = t('disclaimer');
}

// ─── Stop Dropdowns ───────────────────────────────────────────────────────
function populateStopDropdowns() {
    const dataList = document.getElementById('vizagStopsList');
    if (!dataList) return;

    const opts = VIZAG_DATA.stops
        .sort((a, b) => a.name.localeCompare(b.name))
        .map(s => `<option value="${s.name}"></option>`)
        .join('');

    dataList.innerHTML = opts;
}

// ─── Route Finder ─────────────────────────────────────────────────────────
function initRouteFinder() {
    const form = document.getElementById('routeFinderForm');
    const swapBtn = document.getElementById('swapStops');

    swapBtn?.addEventListener('click', () => {
        const from = document.getElementById('fromStop');
        const to = document.getElementById('toStop');
        [from.value, to.value] = [to.value, from.value];
        swapBtn.style.transform = 'rotate(360deg)';
        setTimeout(() => { swapBtn.style.transform = ''; }, 400);
    });

    form?.addEventListener('submit', (e) => {
        e.preventDefault();
        searchRoutes();
    });
}

function searchRoutes() {
    const fromNameStr = document.getElementById('fromStop').value.trim();
    const toNameStr = document.getElementById('toStop').value.trim();

    if (!fromNameStr || !toNameStr) {
        shakeElement(document.querySelector('.route-finder-widget'));
        return;
    }
    if (fromNameStr.toLowerCase() === toNameStr.toLowerCase()) {
        showResultsError('From and To stops cannot be the same.');
        return;
    }

    const fromStopObj = VIZAG_DATA.stops.find(s => s.name.toLowerCase() === fromNameStr.toLowerCase());
    const toStopObj = VIZAG_DATA.stops.find(s => s.name.toLowerCase() === toNameStr.toLowerCase());

    if (!fromStopObj || !toStopObj) {
        showResultsError('Please select valid bus stops from the list.');
        return;
    }

    const fromId = fromStopObj.id;
    const toId = toStopObj.id;

    const matchedRoutes = VIZAG_DATA.routes.filter(route => {
        const idx1 = route.stops.indexOf(fromId);
        const idx2 = route.stops.indexOf(toId);
        return idx1 !== -1 && idx2 !== -1;
    });

    renderResults(fromId, toId, matchedRoutes);
}

function renderResults(fromId, toId, routes) {
    const section = document.getElementById('results');
    const container = document.getElementById('resultsContainer');
    const fromName = getStopName(fromId);
    const toName = getStopName(toId);

    section.classList.add('visible');
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });

    let html = '';

    if (routes.length === 0) {
        html = `<div class="card" style="text-align:center;padding:2.5rem">
      <div style="font-size:3rem;margin-bottom:1rem">🚌</div>
      <h3 style="margin-bottom:0.5rem">${t('noRoutes')}</h3>
      <p style="color:var(--text-secondary);font-size:0.88rem">Try selecting nearby stops or check the Tourist Spot Finder section below.</p>
    </div>`;
    } else {
        const crowdNow = getCurrentCrowd();
        let totalFare = 0;

        routes.forEach(route => {
            const fromIdx = route.stops.indexOf(fromId);
            const toIdx = route.stops.indexOf(toId);
            const stopsCount = Math.abs(toIdx - fromIdx);
            const fare = Math.max(route.baseFare, Math.round(stopsCount * route.baseFare / route.stops.length * 1.8));
            totalFare += fare;

            // Estimated time proportional to distance
            const timeEst = Math.round(stopsCount * route.typicalTimeMin / (route.stops.length - 1));

            const typeCode = route.typeCode;
            const crowdDisplay = route.crowdLevel;

            html += `
      <div class="bus-result-card" onclick="highlightRoute('${route.id}', '${fromId}', '${toId}', ${fare})">
        <div class="bus-number-badge ${typeCode.toLowerCase()}">
          <span>${route.number}</span>
        </div>
        <div class="bus-info">
          <div class="bus-name">
            ${route.name}
            <span class="tag tag-${typeCode.toLowerCase()}" style="margin-left:8px">${route.type}</span>
          </div>
          <div class="bus-stops-preview">
            🏁 ${fromName} → ${toName} · ${stopsCount} stop${stopsCount !== 1 ? 's' : ''}${route.distanceKm ? ` · ${route.distanceKm} km` : ''}
          </div>
          <div style="font-size:0.78rem;color:var(--text-muted);margin-top:4px">${route.note || 'Regular APSRTC Service'}</div>
        </div>
        <div class="bus-meta">
          <div class="bus-fare">₹${fare}</div>
          <div class="bus-time">⏱ ~${timeEst} min</div>
          <div class="crowd-indicator ${crowdClass(crowdDisplay)}">
            <div class="crowd-dot"></div>
            <span>${crowdDisplay.charAt(0).toUpperCase() + crowdDisplay.slice(1)} crowd</span>
          </div>
        </div>
      </div>`;
        });

        // Inline tips removed, moved to side bubble
    }

    container.innerHTML = html;
}

function generateSmartTips(routes, totalFare) {
    const tips = [];
    const oneDayPass = VIZAG_DATA.fares.oneDayPass;
    const hour = new Date().getHours();

    // One-day pass suggestion
    if (totalFare >= oneDayPass) {
        tips.push(`Consider buying a <strong>One Day Pass (₹${oneDayPass})</strong> — your fare exceeds this amount, making the pass a better deal!`);
    }

    // Metro Express suggestion
    const hasCO = routes.some(r => r.typeCode === 'CO');
    const hasME = routes.some(r => r.typeCode === 'ME');
    if (hasCO && hasME) {
        tips.push('A <strong>Metro Express</strong> option is available — slightly costlier but significantly faster and less crowded.');
    }

    // Peak hour warning
    if ((hour >= 7 && hour <= 9) || (hour >= 17 && hour <= 19)) {
        tips.push('🚨 You\'re travelling during <strong>peak hours</strong>. Expect heavy crowds. Consider leaving 20 mins earlier or later.');
    } else if (hour >= 10 && hour <= 16) {
        tips.push('✅ Great timing! You\'re travelling during <strong>off-peak hours</strong> — expect comfortable, less crowded buses.');
    }

    // Last bus warning
    if (hour >= 20) {
        tips.push('⚠️ Last buses typically run between 21:00–22:30. Plan your return journey accordingly.');
    }

    // Fastest route
    if (routes.length > 1) {
        const fastest = [...routes].sort((a, b) => a.typicalTimeMin - b.typicalTimeMin)[0];
        tips.push(`🏃 Fastest option: <strong>Bus ${fastest.number}</strong> (~${fastest.typicalTimeMin} min total route time).`);
    }

    // Student/senior concession
    tips.push('🎓 Students & seniors get <strong>50% concession</strong> — carry your ID card and request at boarding.');

    return tips;
}

function showResultsError(msg) {
    const section = document.getElementById('results');
    const container = document.getElementById('resultsContainer');
    section.classList.add('visible');
    container.innerHTML = `<div class="card" style="text-align:center;padding:2rem;color:var(--secondary)">${msg}</div>`;
}

function shakeElement(el) {
    el?.classList.add('shake');
    setTimeout(() => el?.classList.remove('shake'), 500);
}

// ─── Tourist Spot Finder ──────────────────────────────────────────────────
function initTouristFinder() {
    const select = document.getElementById('touristSelect');
    const resultDiv = document.getElementById('touristResult');

    if (!select || !resultDiv) return;

    // Populate
    select.innerHTML = '<option value="">-- Choose a tourist spot --</option>' +
        VIZAG_DATA.touristSpots.map(s => `<option value="${s.id}">${s.name}</option>`).join('');

    select.addEventListener('change', () => {
        const spot = VIZAG_DATA.touristSpots.find(s => s.id === select.value);
        if (!spot) { resultDiv.classList.remove('visible'); return; }

        const routeDetails = spot.routes
            .map(rId => {
                const route = VIZAG_DATA.routes.find(r => r.id === rId);
                if (!route) return '';
                return `<div class="spot-bus-chip">
          <span class="tag tag-${route.typeCode.toLowerCase()}">${route.typeCode}</span>
          Bus ${route.number}
        </div>`;
            }).join('');

        resultDiv.classList.add('visible');
        resultDiv.innerHTML = `
      <h3>📍 ${spot.name}</h3>
      <p class="spot-desc">${spot.description}</p>
      <div style="font-size:0.82rem;color:var(--text-secondary);margin-bottom:0.75rem">
        🚌 <strong>Nearest Stop:</strong> ${getStopName(spot.nearestStop)}
      </div>
      <div style="font-size:0.82rem;color:var(--text-secondary);margin-bottom:0.75rem">
        <strong>Buses:</strong>
      </div>
      <div class="spot-buses">${routeDetails}</div>
      <div class="spot-tip">💡 ${spot.tips}</div>
    `;
    });
}

// ─── Timetable ────────────────────────────────────────────────────────────
function initTimetable() {
    const select = document.getElementById('timetableRoute');
    const grid = document.getElementById('timetableGrid');
    if (!select || !grid) return;

    // Populate route options
    select.innerHTML = '<option value="">-- Select a Route --</option>' +
        Object.keys(VIZAG_DATA.timetable).map(rId => {
            const route = VIZAG_DATA.routes.find(r => r.id === rId);
            return route ? `<option value="${rId}">Bus ${route.number} – ${route.name}</option>` : '';
        }).join('');

    select.addEventListener('change', () => renderTimetable(select.value));
}

function renderTimetable(routeId) {
    const grid = document.getElementById('timetableGrid');
    if (!grid) return;

    if (!routeId || !VIZAG_DATA.timetable[routeId]) {
        grid.innerHTML = '<p style="color:var(--text-secondary);font-size:0.88rem">Select a route above to view its timetable.</p>';
        return;
    }

    const times = VIZAG_DATA.timetable[routeId].departures;
    const nowStr = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: false });
    const nowMinutes = timeToMinutes(nowStr);

    // Find next bus
    let nextIdx = -1;
    let minDiff = Infinity;
    times.forEach((t, i) => {
        const diff = timeToMinutes(t) - nowMinutes;
        if (diff >= 0 && diff < minDiff) { minDiff = diff; nextIdx = i; }
    });

    grid.innerHTML = times.map((time, i) =>
        `<div class="time-chip ${i === nextIdx ? 'next' : ''}" title="${i === nextIdx ? 'Next bus' : ''}">${time}${i === nextIdx ? ' ⬅ next' : ''}</div>`
    ).join('');
}

function timeToMinutes(timeStr) {
    const parts = timeStr.split(':');
    return parseInt(parts[0]) * 60 + parseInt(parts[1]);
}

// ─── Map ──────────────────────────────────────────────────────────────────
function initMap() {
    const mapEl = document.getElementById('busMap');
    if (!mapEl) return;

    if (typeof L === 'undefined') {
        console.error('Leaflet not loaded. Map will not initialize.');
        mapEl.innerHTML = '<div style="padding:2rem;text-align:center;color:var(--text-secondary)">⚠️ Map engine failed to load. Please check your internet connection.</div>';
        return;
    }

    try {
        mapInstance = L.map('busMap', {
            center: [17.7231, 83.3012],
            zoom: 12,
            zoomControl: true,
        });

        // OSM Transport map style (OPNVKarte)
        L.tileLayer('https://tile.memomaps.de/tilegen/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://memomaps.de">memomaps.de</a> © <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>',
            maxZoom: 18,
        }).addTo(mapInstance);

        // Custom marker icon
        const busIcon = L.divIcon({
            className: '',
            html: `<div style="
          width:16px;height:16px;border-radius:50% 50% 50% 0;
          background:linear-gradient(135deg,#00d4aa,#7c5cff);
          border:1.5px solid rgba(255,255,255,0.3);
          transform:rotate(-45deg);
          box-shadow:0 2px 6px rgba(0,0,0,0.4);
        "></div>`,
            iconSize: [16, 16],
            iconAnchor: [8, 16],
            popupAnchor: [0, -16],
        });

        // Add all stops
        window.mapMarkers = {};
        VIZAG_DATA.stops.forEach(stop => {
            if (!stop.lat || !stop.lng) return;

            const servingRoutes = VIZAG_DATA.routes.filter(r => r.stops.includes(stop.id));
            const routeList = servingRoutes.length > 0
                ? servingRoutes.map(r => `<span style="background:rgba(0,212,170,0.15);color:#00d4aa;padding:2px 6px;border-radius:4px;font-size:0.65rem;margin:1px">${r.number}</span>`).join(' ')
                : '<em style="font-size:0.7rem;color:#4d6180">No routes</em>';

            window.mapMarkers[stop.id] = L.marker([stop.lat, stop.lng], { icon: busIcon, title: stop.name })
                .addTo(mapInstance)
                .bindPopup(`
                    <div style="min-width:140px">
                        <div style="font-weight:700;margin-bottom:4px">${stop.name}</div>
                        <div style="font-size:0.75rem;margin-bottom:4px">Served by: ${routeList}</div>
                    </div>
                `);
        });

        // Ensure map renders correctly
        setTimeout(() => { mapInstance.invalidateSize(); }, 500);

    } catch (e) {
        console.warn('Map initialization failed:', e);
    }
}

// ─── Chatbot ──────────────────────────────────────────────────────────────
function initChatbot() {
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSendBtn');
    const voiceBtn = document.getElementById('chatVoiceBtn');
    const suggestions = document.querySelectorAll('.chat-suggestion-chip');

    sendBtn?.addEventListener('click', sendChatMessage);
    input?.addEventListener('keydown', e => { if (e.key === 'Enter') sendChatMessage(); });
    voiceBtn?.addEventListener('click', toggleVoiceInput);

    suggestions.forEach(chip => {
        chip.addEventListener('click', () => {
            if (input) input.value = chip.textContent.trim();
            sendChatMessage();
        });
    });

    // Init Web Speech API
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SR();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';
        recognition.onresult = (e) => {
            const transcript = e.results[0][0].transcript;
            if (input) input.value = transcript;
            sendChatMessage();
        };
        recognition.onend = () => {
            isRecording = false;
            voiceBtn?.classList.remove('recording');
            if (voiceBtn) voiceBtn.textContent = '🎤';
        };
    }
}

function showWelcomeChatMessage() {
    setTimeout(() => {
        appendChatMessage('bot', `🙏 నమస్కారం! I'm **MārgaDarshi Assistant**.\n\nI can help you find buses, suggest tips and answer questions about Vizag city buses.\n\nTry asking: "Which bus goes to RK Beach?" or "What is the one-day pass?"`);
    }, 800);
}

function sendChatMessage() {
    const input = document.getElementById('chatInput');
    if (!input) return;
    const text = input.value.trim();
    if (!text) return;

    appendChatMessage('user', text);
    input.value = '';

    setTimeout(() => {
        const reply = getBotReply(text);
        appendChatMessage('bot', reply);
        speakText(reply.replace(/\*\*/g, '').replace(/📍|🚌|💰|⏰|🎫|🚍|✅|🚨|⏱|⚠️|→|🏁|🔴|🟡|🟢/g, ''));
    }, 500 + Math.random() * 400);
}

function getBotReply(text) {
    const lower = text.toLowerCase();

    // Greetings
    if (VIZAG_DATA.chatbot.greetings.some(g => lower.includes(g))) {
        return `👋 Hello! How can I help you today?\nAsk me about bus routes, fares, tourist spots, or anything about Vizag city buses!`;
    }

    // Farewords
    if (VIZAG_DATA.chatbot.farewords.some(g => lower.includes(g))) {
        return `🙏 Thank you for using MārgaDarshi! Have a safe journey! ప్రయాణం శుభంగా సాగాలి! 🚌`;
    }

    // Route finder shortcut
    if ((lower.includes('bus') && lower.includes('from')) || lower.includes('how to reach') || lower.includes('how do i go')) {
        return `🔍 For detailed route search, use the **Route Finder** at the top of the page!\nJust select your From and To stops and tap "Find Buses" 🚌`;
    }

    // Check patterns
    for (const item of VIZAG_DATA.chatbot.responses) {
        if (item.patterns.some(p => lower.includes(p))) {
            return item.reply;
        }
    }

    // Default
    return `🤔 I didn't quite catch that. Try asking about:\n• A specific bus route (e.g., "Bus to Steel Plant")\n• Tourist spots (e.g., "Kailasagiri")\n• Fares & passes\n• Crowd & peak hours`;
}

function appendChatMessage(role, text) {
    const msgs = document.getElementById('chatMessages');
    if (!msgs) return;

    const div = document.createElement('div');
    div.className = `chat-message ${role}`;

    const avatar = role === 'bot'
        ? `<div class="message-avatar bot-avatar">🚌</div>`
        : `<div class="message-avatar user-msg-avatar">👤</div>`;

    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    const time = formatTime();

    div.innerHTML = `
    ${avatar}
    <div>
      <div class="message-bubble">${formattedText}</div>
      <div class="message-time">${time}</div>
    </div>`;

    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}

function toggleVoiceInput() {
    const voiceBtn = document.getElementById('chatVoiceBtn');
    if (!recognition) {
        alert('Voice input is not supported in this browser. Please try Chrome or Edge.');
        return;
    }
    if (isRecording) {
        recognition.stop();
        isRecording = false;
        voiceBtn?.classList.remove('recording');
        if (voiceBtn) voiceBtn.textContent = '🎤';
    } else {
        try {
            recognition.start();
            isRecording = true;
            voiceBtn?.classList.add('recording');
            if (voiceBtn) voiceBtn.textContent = '⏹';
        } catch (e) {
            console.warn('Voice recognition error:', e);
        }
    }
}

function speakText(text) {
    if (!('speechSynthesis' in window)) return;
    const utterance = new SpeechSynthesisUtterance(text.substring(0, 200));
    utterance.lang = 'en-IN';
    utterance.rate = 1;
    utterance.volume = 0.7;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
}

// ─── Community Section ────────────────────────────────────────────────────
function initCommunitySection() {
    const submitBtn = document.getElementById('reportSubmitBtn');
    const loginModal = document.getElementById('loginModal');
    const closeModal = document.getElementById('closeModal');
    const loginForm = document.getElementById('loginForm');

    submitBtn?.addEventListener('click', () => {
        if (!isLoggedIn) {
            loginModal?.classList.add('open');
        } else {
            submitReport();
        }
    });

    closeModal?.addEventListener('click', () => loginModal?.classList.remove('open'));
    loginModal?.addEventListener('click', (e) => {
        if (e.target === loginModal) loginModal.classList.remove('open');
    });

    loginForm?.addEventListener('submit', (e) => {
        e.preventDefault();
        // Demo login
        const email = document.getElementById('loginEmail')?.value;
        demoUser.email = email;
        isLoggedIn = true;
        loginModal?.classList.remove('open');
        if (submitBtn) {
            submitBtn.textContent = '📤 Submit Report';
            submitBtn.style.background = 'linear-gradient(135deg, var(--primary), var(--accent))';
        }
        const loginNote = document.getElementById('loginNote');
        if (loginNote) loginNote.style.display = 'none';
        const loggedNote = document.getElementById('loggedNote');
        if (loggedNote) { loggedNote.style.display = 'flex'; loggedNote.textContent = `✅ Logged in as ${email}`; }
        appendDemoReport();
    });
}

function submitReport() {
    const type = document.getElementById('reportType')?.value;
    const route = document.getElementById('reportRoute')?.value;
    const msg = document.getElementById('reportMessage')?.value;

    if (!type || !msg) { alert('Please fill in all fields.'); return; }

    const reportsContainer = document.getElementById('recentReports');
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true });

    const item = document.createElement('div');
    item.className = 'report-item';
    item.innerHTML = `
    <div class="report-meta">
      <span class="report-type-badge">${type}</span>
      ${route ? `<span class="report-route">Bus ${route}</span>` : ''}
      <span>• Just now • ${demoUser.email.split('@')[0]}</span>
    </div>
    <div class="report-content">${msg}</div>`;

    reportsContainer?.prepend(item);
    document.getElementById('reportMessage').value = '';
    alert('✅ Report submitted! Thank you for helping fellow commuters.');
}

function appendDemoReport() {
    const container = document.getElementById('recentReports');
    if (!container) return;
    const item = document.createElement('div');
    item.className = 'report-item';
    item.innerHTML = `
    <div class="report-meta">
      <span class="report-type-badge">Diversion</span>
      <span class="report-route">Bus 28C</span>
      <span>• 10 mins ago • commuter_vizag</span>
    </div>
    <div class="report-content">Road work near Kancharapalem causing 15-min delay. Bus 28C is taking alternate route via Old Town.</div>`;
    container.prepend(item);
}

// ─── Highlight Route on Map ───────────────────────────────────────────────
window.journeyLegs = [];
window.totalJourneyFare = 0;

function highlightRoute(routeId, fromId, toId, fare) {
    const route = VIZAG_DATA.routes.find(r => r.id === routeId);
    if (!route || !mapInstance) return;

    // Scroll to map
    document.getElementById('map-section')?.scrollIntoView({ behavior: 'smooth' });

    // Hide unrelated markers
    if (window.mapMarkers) {
        Object.keys(window.mapMarkers).forEach(stopId => {
            if (route.stops.includes(stopId)) {
                mapInstance.addLayer(window.mapMarkers[stopId]);
            } else {
                mapInstance.removeLayer(window.mapMarkers[stopId]);
            }
        });
    }

    // Add 'Show All' button if not exists
    let showAllBtn = document.getElementById('showAllStopsBtn');
    if (!showAllBtn) {
        showAllBtn = document.createElement('button');
        showAllBtn.id = 'showAllStopsBtn';
        showAllBtn.className = 'btn btn-primary';
        showAllBtn.style.position = 'absolute';
        showAllBtn.style.top = '10px';
        showAllBtn.style.right = '10px';
        showAllBtn.style.zIndex = '1000';
        showAllBtn.style.fontSize = '0.85rem';
        showAllBtn.style.padding = '0.5rem 1rem';
        showAllBtn.textContent = '👁️ Show All Stops';
        showAllBtn.onclick = () => {
            if (window.mapMarkers) {
                Object.values(window.mapMarkers).forEach(m => mapInstance.addLayer(m));
            }
            if (window._routeLine) mapInstance.removeLayer(window._routeLine);
            showAllBtn.style.display = 'none';
            mapInstance.setView([17.7231, 83.3012], 12);
        };
        document.getElementById('busMap').appendChild(showAllBtn);
    }
    showAllBtn.style.display = 'flex';

    // Draw route line with slight delay to wait for scroll
    setTimeout(() => {
        const coords = route.stops
            .map(sid => VIZAG_DATA.stops.find(s => s.id === sid))
            .filter(Boolean)
            .map(s => [s.lat, s.lng]);

        if (window._routeLine) mapInstance.removeLayer(window._routeLine);
        window._routeLine = L.polyline(coords, {
            color: route.typeCode === 'ME' ? '#7c5cff' : '#00d4aa',
            weight: 4, opacity: 0.8, dashArray: route.typeCode === 'ME' ? null : '8, 4',
        }).addTo(mapInstance);

        mapInstance.fitBounds(window._routeLine.getBounds(), { padding: [40, 40] });

        // Open Side Bubble for Tips & Journey Planner
        openSideBubble(route, fare, toId);
    }, 600);
}

function openSideBubble(route, fare, toId) {
    const bubble = document.getElementById('sideBubble');
    const content = document.getElementById('sideBubbleContent');
    if (!bubble || !content) return;

    // Render HTML inside bubble (Removed Smart Tips as per Phase 4)
    let html = `
      <h4>📍 Route Details: <br><span style="color:var(--primary)">${route.number}</span></h4>
      <p>${route.name}</p>
      <div class="journey-summary-box">
        <div><strong>Type:</strong> ${route.typeCode === 'ME' ? 'Metro Express' : 'City Ordinary'}</div>
        <div><strong>Current Leg Fare:</strong> ₹${fare}</div>
        <div><strong>Total Journey Fare:</strong> ₹${window.totalJourneyFare + fare}</div>
      </div>
      
      <div style="margin-top:1.5rem; text-align:center;">
          <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.5rem">Want to travel to another place today?</p>
          <button class="btn btn-outline" style="width:100%" onclick="addJourneyLeg(${fare}, '${toId}')">➕ Add Next Destination</button>
      </div>
    `;

    content.innerHTML = html;
    bubble.classList.add('open');
}

function addJourneyLeg(fare, nextFromId) {
    window.totalJourneyFare += fare;
    window.journeyLegs.push({ fare });
    document.getElementById('sideBubble').classList.remove('open');

    // Trigger One Day Pass alert popup if cumulative fare >= 100
    if (window.totalJourneyFare >= 100) {
        showOneDayPassPopup(window.totalJourneyFare);
    } else {
        showResultsError(`Leg added! Total fare so far: ₹${window.totalJourneyFare}. Search your next stop!`, true);
    }

    // Reset route finder to start from the current destination
    const fromSel = document.getElementById('fromStop');
    const toSel = document.getElementById('toStop');
    if (fromSel) {
        const nextStopObj = VIZAG_DATA.stops.find(s => s.id === nextFromId);
        fromSel.value = nextStopObj ? nextStopObj.name : '';
    }
    if (toSel) {
        toSel.value = "";
    }

    // Scroll back to route finder
    document.getElementById('hero')?.scrollIntoView({ behavior: 'smooth' });
}

function showOneDayPassPopup(totalFare) {
    const pop = document.createElement('div');
    pop.className = 'modal-overlay open';
    pop.innerHTML = `
        <div class="modal modal-relative" style="text-align:center; padding:3rem 2rem;">
            <div style="font-size:4rem; margin-bottom:1rem;">🎫</div>
            <h2 style="color: var(--brand-secondary)">Get a One Day Pass!</h2>
            <p style="margin: 1rem 0; font-size: 1.1rem">Your total travel fare so far is <strong>₹${totalFare}</strong>.</p>
            <p style="color: var(--text-secondary); margin-bottom:2rem;">Since you have exceeded ₹100, it is <strong>highly recommended</strong> to ask your conductor for a One Day Pass (₹100) to save money on unlimited City Ordinary rides today!</p>
            <button class="btn btn-primary" onclick="this.parentElement.parentElement.remove()" style="width:100%">Got It, Thanks!</button>
        </div>
    `;
    document.body.appendChild(pop);
}

// ─── Phase 4 Modal Hooks & Bus Search ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Basic modal closing
    document.getElementById('closeSideBubble')?.addEventListener('click', () => {
        document.getElementById('sideBubble')?.classList.remove('open');
    });

    // Smart Tips & Know Your Bus
    const tipsBtn = document.getElementById('openTipsBtn');
    const tipsModal = document.getElementById('smartTipsModal');
    const knowBusModal = document.getElementById('knowYourBusModal');

    tipsBtn?.addEventListener('click', () => tipsModal?.classList.add('open'));
    document.getElementById('closeTipsModal')?.addEventListener('click', () => tipsModal?.classList.remove('open'));

    document.getElementById('openKnowYourBusBtn')?.addEventListener('click', () => {
        tipsModal?.classList.remove('open');
        knowBusModal?.classList.add('open');
    });
    document.getElementById('closeKnowBusModal')?.addEventListener('click', () => knowBusModal?.classList.remove('open'));

    // Bus Search Modal
    const busSearchModal = document.getElementById('busSearchModal');
    const busNumInput = document.getElementById('busNumberInput');
    const busSearchRes = document.getElementById('busSearchModal_results');

    document.getElementById('navBusSearchDesktop')?.addEventListener('click', (e) => { e.preventDefault(); busSearchModal?.classList.add('open'); setTimeout(() => busNumInput?.focus(), 100); });
    document.getElementById('navBusSearchMobile')?.addEventListener('click', (e) => { e.preventDefault(); busSearchModal?.classList.add('open'); document.getElementById('mobileMenu')?.classList.remove('active'); });
    document.getElementById('closeBusSearchModal')?.addEventListener('click', () => busSearchModal?.classList.remove('open'));

    busNumInput?.addEventListener('input', (e) => {
        const query = e.target.value.trim().toLowerCase();
        if (!query) { busSearchRes.innerHTML = ''; return; }

        const matches = VIZAG_DATA.routes.filter(r => r.number.toLowerCase().includes(query));
        if (matches.length === 0) {
            busSearchRes.innerHTML = '<p style="color:var(--text-muted); text-align:center;">No buses found for this number.</p>';
            return;
        }

        let html = '';
        matches.forEach(r => {
            const stopsTxt = r.stops.map(getStopName).filter(Boolean);
            const firstStop = stopsTxt[0] || '?';
            const lastStop = stopsTxt[stopsTxt.length - 1] || '?';
            html += `
            <div class="card" style="padding:1rem; margin-bottom:1rem; background: rgba(255,255,255,0.02)">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem">
                    <span class="bus-number-badge ${r.typeCode.toLowerCase()}" style="font-size: 1rem; padding: 4px 8px">${r.number}</span>
                    <span class="tag tag-${r.typeCode.toLowerCase()}">${r.type}</span>
                </div>
                <h4 style="margin-bottom:0.5rem">${r.name}</h4>
                <div style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.5rem">
                    🏁 ${firstStop} → ${lastStop} (${r.stops.length} stops)
                </div>
                <div style="font-size:0.85rem; display:flex; gap:1rem; color:var(--text-secondary)">
                    <span>💸 ₹${r.baseFare}+</span>
                    <span>⏱ ~${r.typicalTimeMin}m</span>
                    <span>🚶 ${r.crowdLevel} crowd</span>
                </div>
                <div style="margin-top:0.8rem; font-size:0.8rem; color:var(--text-muted); border-top:1px solid var(--border-light); padding-top:0.5rem;">
                    <strong>Route Stops:</strong> ${stopsTxt.join(' → ')}
                </div>
            </div>`;
        });
        busSearchRes.innerHTML = html;
    });
});

// ─── FAQ ──────────────────────────────────────────────────────────────────
function initFAQ() {
    document.querySelectorAll('.faq-question').forEach(btn => {
        btn.addEventListener('click', () => {
            const item = btn.closest('.faq-item');
            const isOpen = item.classList.contains('open');

            // Close all
            document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));

            // Toggle clicked
            if (!isOpen) item.classList.add('open');
        });
    });
}

// ─── Scroll Animations ────────────────────────────────────────────────────
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('visible');
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
}

// ─── Scroll Spy ───────────────────────────────────────────────────────────
function initScrollSpy() {
    const sections = document.querySelectorAll('section[id], div[id]');
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navLinks.forEach(link => {
                    link.style.color = link.getAttribute('href') === `#${id}` ? 'var(--primary)' : '';
                });
            }
        });
    }, { threshold: 0.4 });

    sections.forEach(s => observer.observe(s));
}

// ─── Chat FAB ──────────────────────────────────────────────────────────────
function scrollToChat() {
    document.getElementById('chatbot-section')?.scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => {
        const input = document.getElementById('chatInput');
        input?.focus();
    }, 700);
}

// Add shake animation via CSS injection
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
  @keyframes shake { 0%,100%{transform:translateX(0)} 20%{transform:translateX(-8px)} 40%{transform:translateX(8px)} 60%{transform:translateX(-5px)} 80%{transform:translateX(5px)} }
  .shake { animation: shake 0.5s ease !important; }
`;
document.head.appendChild(shakeStyle);

// Map Fix: Ensure map updates its size correctly
window.addEventListener('resize', () => {
    if (mapInstance) mapInstance.invalidateSize();
});

/* ═══════════════════════════════════════════════════════════════════════════
   VISUAL EFFECTS
   ═══════════════════════════════════════════════════════════════════════════ */

// ── 1. Page Loader ─────────────────────────────────────────────────────────
function initPageLoader() {
    const loader = document.getElementById('pageLoader');
    if (!loader) return;

    // Dismiss when all resources are ready
    const dismiss = () => {
        loader.classList.add('hidden');
    };

    if (document.readyState === 'complete') {
        setTimeout(dismiss, 400);
    } else {
        window.addEventListener('load', () => setTimeout(dismiss, 400));
        // Safety fallback after 3.5s
        setTimeout(dismiss, 3500);
    }
}

// ── 2. Custom Glowing Cursor ───────────────────────────────────────────────
function initCursor() {
    // Only on non-touch, pointer-capable devices
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    const dot = document.getElementById('cursorDot');
    const ring = document.getElementById('cursorRing');
    if (!dot || !ring) return;

    let ringX = 0, ringY = 0;
    let dotX = 0, dotY = 0;
    let rafId;

    document.body.classList.add('cursor-ready');

    document.addEventListener('mousemove', (e) => {
        dotX = e.clientX;
        dotY = e.clientY;

        // Dot follows instantly
        dot.style.left = dotX + 'px';
        dot.style.top = dotY + 'px';

        // Ring follows with smooth lag
        if (!rafId) {
            rafId = requestAnimationFrame(animateRing);
        }
    });

    function animateRing() {
        rafId = null;
        ringX += (dotX - ringX) * 0.12;
        ringY += (dotY - ringY) * 0.12;
        ring.style.left = ringX + 'px';
        ring.style.top = ringY + 'px';

        const dx = dotX - ringX;
        const dy = dotY - ringY;
        if (Math.abs(dx) > 0.5 || Math.abs(dy) > 0.5) {
            rafId = requestAnimationFrame(animateRing);
        }
    }

    // Hover state on interactive elements
    const interactiveSelector = 'a, button, select, input, textarea, [tabindex], .card, .feature-card, .tip-card, .bus-result-card';
    document.addEventListener('mouseover', (e) => {
        if (e.target.closest(interactiveSelector)) {
            document.body.classList.add('cursor-hover');
        }
    });
    document.addEventListener('mouseout', (e) => {
        if (e.target.closest(interactiveSelector)) {
            document.body.classList.remove('cursor-hover');
        }
    });

    // Click burst
    document.addEventListener('mousedown', () => {
        document.body.classList.add('cursor-click');
    });
    document.addEventListener('mouseup', () => {
        document.body.classList.remove('cursor-click');
    });
}

// ── 3. Hero Parallax ──────────────────────────────────────────────────────
function initParallax() {
    const hero = document.getElementById('hero');
    const orbs = hero ? hero.querySelectorAll('.orb') : [];
    if (!orbs.length) return;

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        if (scrollY > window.innerHeight) return; // only in hero range
        orbs.forEach((orb, i) => {
            const speed = 0.08 + i * 0.04;
            orb.style.transform = `translateY(${scrollY * speed}px)`;
        });
    }, { passive: true });

    // Mouse-move parallax inside hero
    hero && hero.addEventListener('mousemove', (e) => {
        const rect = hero.getBoundingClientRect();
        const cx = (e.clientX - rect.left) / rect.width - 0.5; // -0.5 to 0.5
        const cy = (e.clientY - rect.top) / rect.height - 0.5;
        orbs.forEach((orb, i) => {
            const depth = 18 + i * 10;
            orb.style.transform = `translate(${cx * depth}px, ${cy * depth}px)`;
        });
    });
    hero && hero.addEventListener('mouseleave', () => {
        orbs.forEach(orb => orb.style.transform = '');
    });
}

// ── 4. 3D Card Tilt ───────────────────────────────────────────────────────
function initTiltCards() {
    if (!window.matchMedia('(hover: hover)').matches) return;

    // Apply tilt to feature and tip cards
    const selector = '.feature-card, .tip-card, .bus-type-card';
    document.querySelectorAll(selector).forEach(card => {
        card.classList.add('tilt-card');

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const cx = (e.clientX - rect.left) / rect.width - 0.5;
            const cy = (e.clientY - rect.top) / rect.height - 0.5;
            const rotX = cy * -10;  // tilt up/down
            const rotY = cx * 12;  // tilt left/right
            card.style.transform = `perspective(600px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-4px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

// ── 5. Ripple on Buttons ──────────────────────────────────────────────────
function initRippleButtons() {
    const rippleTargets = '.btn, .search-btn, .chat-send-btn, .lang-btn, .swap-btn';
    document.querySelectorAll(rippleTargets).forEach(btn => {
        btn.classList.add('ripple-host');
        btn.addEventListener('click', (e) => {
            const rect = btn.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height) * 1.4;
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            const ripple = document.createElement('span');
            ripple.className = 'ripple-wave';
            ripple.style.cssText = `width:${size}px;height:${size}px;left:${x}px;top:${y}px`;
            btn.appendChild(ripple);
            ripple.addEventListener('animationend', () => ripple.remove());
        });
    });
}

// ── 6. Button Spotlight (mouse-position radial gradient) ──────────────────
function initButtonSpotlight() {
    document.querySelectorAll('.btn-primary, .search-btn').forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width * 100).toFixed(1);
            const y = ((e.clientY - rect.top) / rect.height * 100).toFixed(1);
            btn.style.setProperty('--mx', `${x}%`);
            btn.style.setProperty('--my', `${y}%`);
        });
    });
}

// ── 7. Stat Count-Up Animation ────────────────────────────────────────────
function initStatCountUp() {
    const statNumbers = document.querySelectorAll('.hero-stat .number');
    if (!statNumbers.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            observer.unobserve(entry.target);

            const el = entry.target;
            const rawText = el.textContent.trim(); // e.g. "35+" or "100+"
            const suffix = rawText.replace(/[\d.]/g, '');  // keep "+" etc
            const target = parseFloat(rawText) || 0;
            const duration = 1200;
            const start = performance.now();

            function tick(now) {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                // Ease-out cubic
                const eased = 1 - Math.pow(1 - progress, 3);
                el.textContent = Math.round(eased * target) + suffix;
                if (progress < 1) requestAnimationFrame(tick);
            }
            requestAnimationFrame(tick);
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(el => observer.observe(el));
}
