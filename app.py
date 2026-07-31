
"""
SOLDIER UNPLUGGED | SSB Practice Tool
PPDT + TAT | Exact Real SSB Timing
Created by Ayush Kumar

Logic:
  - data/ppdt.pdf → 100 PPDT pics
  - data/tat.pdf  → 100 TAT pics
  - User chooses how many pics per session
  - Days auto-created (Day 1 = 1..N, Day 2 = N+1..2N ...)
  - Sequential, no random repeat
"""
import streamlit as st
import time
import math
from utils.image_utils import load_ppdt_images, load_tat_images, generate_placeholder

st.set_page_config(page_title="Soldier Unplugged | SSB Practice", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Roboto+Condensed:wght@400;700&display=swap');
:root{--gold:#c9a227;--olive:#3d5a3d;--dark:#0d1a0d;--sand:#d4c5a0;}
.stApp{background:linear-gradient(180deg,#0d1a0d 0%,#152515 50%,#1e321e 100%);color:#e8e4d9;}
h1,h2,h3{font-family:'Oswald',sans-serif!important;color:var(--gold)!important;letter-spacing:1px;}
p,li,label,.stMarkdown{font-family:'Roboto Condensed',sans-serif;color:#e8e4d9;}
.main-header{background:linear-gradient(90deg,#0d1a0d,#2a4a2a,#0d1a0d);border:2px solid var(--gold);
  border-radius:10px;padding:1.1rem 1.4rem;text-align:center;margin-bottom:1.4rem;
  box-shadow:0 0 22px rgba(201,162,39,0.3);}
.main-header h1{margin:0;font-size:2.3rem;text-shadow:0 0 12px rgba(201,162,39,0.55);}
.main-header .sub{color:var(--sand);letter-spacing:2px;font-size:1rem;margin-top:4px;}
.main-header .by{color:#999;font-size:0.82rem;margin-top:3px;}
.instruction-box{background:rgba(25,45,25,0.92);border-left:5px solid var(--gold);
  padding:1.1rem 1.3rem;border-radius:0 10px 10px 0;margin:1rem 0;line-height:1.55;}
.timer-big{font-family:'Oswald',sans-serif;font-size:4.2rem;color:var(--gold);text-align:center;
  background:#0a150a;border:4px solid var(--gold);border-radius:14px;padding:0.6rem 1.8rem;
  margin:1.2rem auto;max-width:320px;box-shadow:0 0 30px rgba(201,162,39,0.35);}
.timer-red{color:#ff4444!important;border-color:#ff4444!important;animation:pulse 0.7s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.55}}
.phase{display:inline-block;background:var(--olive);color:var(--gold);font-family:'Oswald',sans-serif;
  padding:0.35rem 1rem;border-radius:5px;font-size:1.05rem;letter-spacing:1.5px;margin-bottom:0.9rem;}
.start-write{font-family:'Oswald',sans-serif;font-size:2.8rem;color:#00e676;text-align:center;
  background:#0a1f0a;border:4px solid #00e676;border-radius:14px;padding:1.2rem;margin:1.5rem auto;
  max-width:520px;box-shadow:0 0 35px rgba(0,230,118,0.4);letter-spacing:3px;}
.stop-box{font-family:'Oswald',sans-serif;font-size:3.2rem;color:#ff3333;text-align:center;
  background:#1a0505;border:5px solid #ff3333;border-radius:14px;padding:1.4rem;margin:1.5rem auto;
  max-width:520px;box-shadow:0 0 40px rgba(255,50,50,0.5);letter-spacing:4px;animation:pulse 0.6s infinite;}
.bell{font-size:4rem;text-align:center;margin:0.5rem 0;}
.day-card{background:rgba(30,55,30,0.75);border:1px solid var(--olive);border-radius:8px;padding:0.85rem 1.1rem;margin:0.35rem 0;}
.stButton>button{background:linear-gradient(180deg,#3d5a3d,#2a402a)!important;color:var(--gold)!important;
  border:2px solid var(--gold)!important;font-family:'Oswald',sans-serif!important;font-size:1.05rem!important;
  letter-spacing:1.5px;padding:0.5rem 1.4rem!important;border-radius:7px!important;}
.stButton>button:hover{background:linear-gradient(180deg,#4a6b4a,#3d5a3d)!important;
  box-shadow:0 0 16px rgba(201,162,39,0.45);}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0a150a,#152515);border-right:2px solid var(--olive);}
div[data-testid="stImage"]{border:3px solid var(--gold);border-radius:8px;overflow:hidden;}
.footer{text-align:center;padding:1.3rem;margin-top:2rem;border-top:1px solid var(--olive);color:#777;font-size:0.82rem;}
</style>
""", unsafe_allow_html=True)

def init():
    defaults = {
        "module": None, "phase": "setup", "all_images": [],
        "day_images": [], "pic_index": 0, "sub_phase": None,
        "timer_start": None, "chunk_size": 12, "day_num": 1,
        "total_days": 1, "pics_in_day": 12,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

def header():
    import base64
    from pathlib import Path
    logo_path = Path(__file__).parent / "assets" / "logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:52px;vertical-align:middle;margin-right:12px;">'
    else:
        logo_html = "🎖️"
    st.markdown(f"""
    <div class="main-header">
      <h1>{logo_html} SOLDIER UNPLUGGED</h1>
      <div class="sub">SSB PRACTICE TOOL — PPDT • TAT</div>
      <div class="by">Created by Ayush Kumar &nbsp;|&nbsp; Exact Real SSB Timing &nbsp;|&nbsp; Free for Every Aspirant</div>
    </div>
    """, unsafe_allow_html=True)

def big_timer(seconds, alert_at=10):
    ph = st.empty()
    if st.session_state.timer_start is None:
        st.session_state.timer_start = time.time()
    rem = max(0, seconds - (time.time() - st.session_state.timer_start))
    m, s = int(rem // 60), int(rem % 60)
    cls = "timer-big timer-red" if rem <= alert_at else "timer-big"
    ph.markdown(f'<div class="{cls}">{m:02d}:{s:02d}</div>', unsafe_allow_html=True)
    return rem

def reset_timer():
    st.session_state.timer_start = time.time()

def play_bell():
    st.markdown('<div class="bell">🔔</div>', unsafe_allow_html=True)
    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function() {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      function beep(freq, duration, delay) {
        setTimeout(function() {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.frequency.value = freq;
          gain.gain.setValueAtTime(0.45, ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration);
          osc.start(ctx.currentTime);
          osc.stop(ctx.currentTime + duration);
        }, delay);
      }
      // Triple bell sound
      beep(880, 0.35, 0);
      beep(660, 0.40, 320);
      beep(990, 0.50, 650);
    })();
    </script>
    """, height=0)

def make_days(images, chunk):
    """Split ordered images into days of size `chunk`."""
    days = []
    total = len(images)
    num_days = max(1, math.ceil(total / chunk))
    for i in range(num_days):
        start = i * chunk
        end = min(start + chunk, total)
        days.append(images[start:end])
    return days

@st.cache_data(show_spinner="Loading PPDT pictures…")
def get_ppdt():
    return load_ppdt_images()

@st.cache_data(show_spinner="Loading TAT pictures…")
def get_tat():
    return load_tat_images()

with st.sidebar:
    st.markdown("### 🎖️ NAVIGATION")
    nav = st.radio("", ["🏠 Home", "🖼️ PPDT", "📖 TAT", "ℹ️ About"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("#### 📁 PDFs")
    st.caption("data/ppdt.pdf → PPDT")
    st.caption("data/tat.pdf → TAT")
    st.markdown("---")
    st.markdown('<div style="font-size:0.78rem;color:#888;text-align:center;"><b>SOLDIER UNPLUGGED</b><br>by Ayush Kumar</div>', unsafe_allow_html=True)

header()

# ═══════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════
if nav == "🏠 Home":
    st.markdown("""
    <div class="instruction-box">
    <h3>Welcome, Future Officer!</h3>
    <p>Exact SSB timing. <b>No writing box</b> — write on your own paper.</p>
    <ul>
      <li>Pehle choose karo <b>kitni pictures per session</b></li>
      <li>Tool automatically <b>Day 1, Day 2, Day 3…</b> bana dega</li>
      <li>Har Day sequential pictures (no random, no repeat)</li>
      <li>Jo Day kar chuke, next Day pe jaao</li>
    </ul>
    <pre style="background:#0a150a;padding:10px;border-radius:6px;">data/ppdt.pdf   ← 100 PPDT pictures
data/tat.pdf    ← 100 TAT pictures</pre>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PPDT
# ═══════════════════════════════════════════════════════════════
elif nav == "🖼️ PPDT":
    if st.session_state.module != "PPDT":
        st.session_state.module = "PPDT"
        st.session_state.phase = "setup"
        st.session_state.all_images = get_ppdt()

    # STEP 1: Setup — choose chunk size → days form
    if st.session_state.phase == "setup":
        total = len(st.session_state.all_images)
        st.markdown(f"### PPDT &nbsp;•&nbsp; {total} pictures loaded")
        st.markdown("""
        <div class="instruction-box">
        <p>Choose how many pictures you want in <b>one session/Day</b>.
        Tool will divide all pictures into Day 1, Day 2, Day 3… sequentially.</p>
        <p>Example: 100 pics + 10 per day = 10 Days. Day 1 = pics 1-10, Day 2 = 11-20…</p>
        </div>
        """, unsafe_allow_html=True)
        chunk = st.slider("Pictures per Day / Session", 1, min(20, total), 1, key="ppdt_chunk")
        st.session_state.chunk_size = chunk
        days = make_days(st.session_state.all_images, chunk)
        st.session_state.total_days = len(days)
        st.info(f"**{len(days)} Days** will be created (each with up to {chunk} picture(s))")
        if st.button("→ Continue to Day Selection", use_container_width=True):
            st.session_state.phase = "select_day"
            st.rerun()

    # STEP 2: Select Day
    elif st.session_state.phase == "select_day":
        total = len(st.session_state.all_images)
        chunk = st.session_state.chunk_size
        days = make_days(st.session_state.all_images, chunk)
        st.markdown(f"### PPDT — Select Day ({len(days)} Days available)")
        st.caption(f"Total pictures: {total} | Per day: {chunk}")
        for i, day_imgs in enumerate(days):
            start_no = i * chunk + 1
            end_no = start_no + len(day_imgs) - 1
            cols = st.columns([5, 1])
            with cols[0]:
                st.markdown(f'<div class="day-card"><b>Day {i+1}</b> &nbsp;•&nbsp; Pictures {start_no}–{end_no} &nbsp;({len(day_imgs)} pics)</div>', unsafe_allow_html=True)
            with cols[1]:
                if st.button("Select", key=f"ppdt_day_{i}"):
                    st.session_state.day_num = i + 1
                    st.session_state.day_images = day_imgs
                    st.session_state.pics_in_day = len(day_imgs)
                    st.session_state.pic_index = 0
                    st.session_state.phase = "instructions"
                    st.rerun()
        if st.button("← Change pictures per day"):
            st.session_state.phase = "setup"
            st.rerun()

    # STEP 3: Instructions
    elif st.session_state.phase == "instructions":
        st.markdown(f"### PPDT — Day {st.session_state.day_num} &nbsp;•&nbsp; {st.session_state.pics_in_day} picture(s)")
        st.markdown("""
        <div class="instruction-box">
        <h3>📋 PPDT Instructions (Exactly as given in SSB)</h3>
        <p>You will be shown <b>one hazy picture</b> for <b>30 seconds</b>.</p>
        <p>Observe: Number of characters, age, sex (M/F/P), mood (+/−/0), situation.</p>
        <p>After 30 sec → <b>START WRITING</b></p>
        <p><b>1 minute</b> — Character Box on your paper</p>
        <p><b>4 minutes</b> — Full story (Past → Present → Action → Positive Outcome)</p>
        <p>Time over → <b>🔔 BELL + STOP</b></p>
        <p>If multiple pictures in this Day, next picture starts automatically after STOP.</p>
        <p><b>Write on your own paper.</b></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("▶ START PPDT — Day " + str(st.session_state.day_num), use_container_width=True):
            st.session_state.phase = "running"
            st.session_state.sub_phase = "view"
            st.session_state.pic_index = 0
            reset_timer()
            st.rerun()
        if st.button("← Back to Day Selection"):
            st.session_state.phase = "select_day"
            st.rerun()

    # STEP 4: Running
    elif st.session_state.phase == "running":
        idx = st.session_state.pic_index
        total_in_day = st.session_state.pics_in_day
        img = st.session_state.day_images[idx]

        if st.session_state.sub_phase == "view":
            st.markdown(f'<div class="phase">DAY {st.session_state.day_num} — PIC {idx+1}/{total_in_day} — OBSERVE 30s</div>', unsafe_allow_html=True)
            st.warning("Look carefully. Do NOT write yet.")
            rem = big_timer(30, 5)
            st.image(img, use_container_width=True)
            if rem <= 0:
                st.session_state.sub_phase = "write_box"
                reset_timer()
                st.rerun()
            else:
                time.sleep(0.15)
                st.rerun()

        elif st.session_state.sub_phase == "write_box":
            st.markdown(f'<div class="phase">DAY {st.session_state.day_num} — PIC {idx+1}/{total_in_day} — CHARACTER BOX</div>', unsafe_allow_html=True)
            st.markdown('<div class="start-write">START WRITING</div>', unsafe_allow_html=True)
            st.info("Paper pe: No. of characters • Sex (M/F/P) • Age • Mood (+/−/0) • Circle Hero")
            rem = big_timer(60, 10)
            if rem <= 0:
                st.session_state.sub_phase = "write_story"
                reset_timer()
                st.rerun()
            else:
                time.sleep(0.15)
                st.rerun()

        elif st.session_state.sub_phase == "write_story":
            st.markdown(f'<div class="phase">DAY {st.session_state.day_num} — PIC {idx+1}/{total_in_day} — STORY</div>', unsafe_allow_html=True)
            st.markdown('<div class="start-write">CONTINUE WRITING YOUR STORY</div>', unsafe_allow_html=True)
            st.info("Past → Present → Action (OLQs) → Positive Outcome")
            rem = big_timer(240, 30)
            if rem <= 0:
                if idx + 1 < total_in_day:
                    # next picture in same day
                    st.session_state.pic_index += 1
                    st.session_state.sub_phase = "view"
                    reset_timer()
                else:
                    st.session_state.phase = "stop"
                st.rerun()
            else:
                time.sleep(0.2)
                st.rerun()

    # STEP 5: STOP
    elif st.session_state.phase == "stop":
        play_bell()
        st.markdown('<div class="stop-box">🔔 STOP</div>', unsafe_allow_html=True)
        st.markdown('<div class="bell">BELL RANG — STOP WRITING</div>', unsafe_allow_html=True)
        st.success(f"Day {st.session_state.day_num} complete! ({st.session_state.pics_in_day} picture(s) done)")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("→ Next Day / Select Day", use_container_width=True):
                st.session_state.phase = "select_day"
                st.rerun()
        with c2:
            if st.button("← Change setup", use_container_width=True):
                st.session_state.phase = "setup"
                st.rerun()

# ═══════════════════════════════════════════════════════════════
# TAT
# ═══════════════════════════════════════════════════════════════
elif nav == "📖 TAT":
    if st.session_state.module != "TAT":
        st.session_state.module = "TAT"
        st.session_state.phase = "setup"
        st.session_state.all_images = get_tat()

    # STEP 1: Setup
    if st.session_state.phase == "setup":
        total = len(st.session_state.all_images)
        st.markdown(f"### TAT &nbsp;•&nbsp; {total} pictures loaded")
        st.markdown("""
        <div class="instruction-box">
        <p>Choose how many pictures per <b>Day / Session</b> (real SSB = 12).</p>
        <p>Tool divides all pictures sequentially into Day 1, Day 2, Day 3…</p>
        <p>Example: 100 pics + 12 per day = 9 Days (last day may have fewer).</p>
        </div>
        """, unsafe_allow_html=True)
        chunk = st.slider("Pictures per Day (recommended 12)", 1, min(20, total), 12, key="tat_chunk")
        st.session_state.chunk_size = chunk
        days = make_days(st.session_state.all_images, chunk)
        st.info(f"**{len(days)} Days** will be created")
        if st.button("→ Continue to Day Selection", use_container_width=True):
            st.session_state.phase = "select_day"
            st.rerun()

    # STEP 2: Select Day
    elif st.session_state.phase == "select_day":
        chunk = st.session_state.chunk_size
        days = make_days(st.session_state.all_images, chunk)
        st.markdown(f"### TAT — Select Day ({len(days)} Days available)")
        for i, day_imgs in enumerate(days):
            start_no = i * chunk + 1
            end_no = start_no + len(day_imgs) - 1
            cols = st.columns([5, 1])
            with cols[0]:
                st.markdown(f'<div class="day-card"><b>Day {i+1}</b> &nbsp;•&nbsp; Pictures {start_no}–{end_no} &nbsp;({len(day_imgs)} pics)</div>', unsafe_allow_html=True)
            with cols[1]:
                if st.button("Select", key=f"tat_day_{i}"):
                    st.session_state.day_num = i + 1
                    st.session_state.day_images = day_imgs
                    st.session_state.pics_in_day = len(day_imgs)
                    st.session_state.pic_index = 0
                    st.session_state.phase = "instructions"
                    st.rerun()
        if st.button("← Change pictures per day"):
            st.session_state.phase = "setup"
            st.rerun()

    # STEP 3: Instructions
    elif st.session_state.phase == "instructions":
        st.markdown(f"### TAT — Day {st.session_state.day_num} &nbsp;•&nbsp; {st.session_state.pics_in_day} pictures")
        st.markdown("""
        <div class="instruction-box">
        <h3>📋 TAT Instructions (Exactly as given in SSB)</h3>
        <p>For each picture: <b>30 seconds</b> observe → <b>START WRITING</b> → <b>4 minutes</b> story.</p>
        <p>No break between pictures. Continuous.</p>
        <p>Story: Past → Present (thoughts/feelings) → Action (OLQs) → Positive Outcome.</p>
        <p>If this is a full 12-picture day, last one can be treated as blank if you wish.</p>
        <p>Last picture ends → <b>🔔 BELL + STOP</b></p>
        <p><b>Write on your own paper.</b></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶ START TAT — Day {st.session_state.day_num}", use_container_width=True):
            # if exactly 12, make last blank-style optional (keep original image, user knows)
            st.session_state.phase = "running"
            st.session_state.sub_phase = "view"
            st.session_state.pic_index = 0
            reset_timer()
            st.rerun()
        if st.button("← Back to Day Selection"):
            st.session_state.phase = "select_day"
            st.rerun()

    # STEP 4: Running
    elif st.session_state.phase == "running":
        idx = st.session_state.pic_index
        total = st.session_state.pics_in_day
        img = st.session_state.day_images[idx]

        if st.session_state.sub_phase == "view":
            st.markdown(f'<div class="phase">DAY {st.session_state.day_num} — PIC {idx+1}/{total} — OBSERVE 30s</div>', unsafe_allow_html=True)
            st.warning("Look carefully. Do NOT write yet.")
            rem = big_timer(30, 5)
            st.image(img, use_container_width=True)
            if rem <= 0:
                st.session_state.sub_phase = "write"
                reset_timer()
                st.rerun()
            else:
                time.sleep(0.15)
                st.rerun()

        elif st.session_state.sub_phase == "write":
            st.markdown(f'<div class="phase">DAY {st.session_state.day_num} — PIC {idx+1}/{total} — WRITE STORY</div>', unsafe_allow_html=True)
            st.markdown('<div class="start-write">START WRITING</div>', unsafe_allow_html=True)
            st.info("Past → Present → Action (OLQs) → Positive Outcome")
            rem = big_timer(240, 30)
            if rem <= 0:
                if idx + 1 < total:
                    st.session_state.pic_index += 1
                    st.session_state.sub_phase = "view"
                    reset_timer()
                else:
                    st.session_state.phase = "stop"
                st.rerun()
            else:
                time.sleep(0.2)
                st.rerun()

    # STEP 5: STOP
    elif st.session_state.phase == "stop":
        play_bell()
        st.markdown('<div class="stop-box">🔔 STOP</div>', unsafe_allow_html=True)
        st.markdown('<div class="bell">BELL RANG — STOP WRITING</div>', unsafe_allow_html=True)
        st.success(f"Day {st.session_state.day_num} complete! ({st.session_state.pics_in_day} pictures done)")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("→ Next Day / Select Day", use_container_width=True):
                st.session_state.phase = "select_day"
                st.rerun()
        with c2:
            if st.button("← Change setup", use_container_width=True):
                st.session_state.phase = "setup"
                st.rerun()

# ═══════════════════════════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════════════════════════
elif nav == "ℹ️ About":
    st.markdown("""
    <div class="instruction-box">
    <h3>About Soldier Unplugged</h3>
    <p>Created by <b>Ayush Kumar</b>.</p>
    <h4>How days work</h4>
    <ol>
      <li>Load 100 pictures from PDF (order preserved)</li>
      <li>You choose how many pictures per Day</li>
      <li>Tool creates Day 1, Day 2, Day 3… sequentially</li>
      <li>Practice Day by Day — no random, no repeat of same set</li>
    </ol>
    <pre style="background:#0a150a;padding:10px;border-radius:6px;">data/ppdt.pdf
data/tat.pdf</pre>
    <p>Unofficial tool. Not affiliated with SSB/DIPR.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer">SOLDIER UNPLUGGED • by Ayush Kumar • Jai Hind</div>', unsafe_allow_html=True)
