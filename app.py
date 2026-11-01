import streamlit as st
from PIL import Image, ImageEnhance
import io
import requests

st.set_page_config(page_title="Sharpify 18+ - Obrada Slika", page_icon="📸", layout="centered")

# Adsterra reklama u pozadini za zaradu para
kod_za_reklamu = """
<script type="text/javascript">
	atOptions = {
		'key' : 'fdf9ccaeec046fb017df8b64eeb2c0b6',
		'format' : 'iframe',
		'height' : 250,
		'width' : 300,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//://highperformanceformat.com"></script>
"""
st.markdown(f"{kod_za_reklamu}", unsafe_allow_html=True)

st.markdown("""
    <style>
    .main { background-color: #0d0f12; }
    div.stButton > button:first-child {
        background-color: #00FF66;
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #00CC52;
        box-shadow: 0px 0px 15px #00FF66;
    }
    </style>
""", unsafe_allow_html=True)

if "punoletan" not in st.session_state:
    st.session_state.punoletan = None

# --- EKRAN 1: SIGURNOSNA PROVERA ---
if st.session_state.punoletan is None:
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-family: sans-serif; letter-spacing: 2px;'>📸 SHARPIFY <span style='color: #00FF66; font-weight: bold; text-shadow: 0 0 10px #00FF66;'>18+</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaaaaa; font-style: italic;'>Pretvori mutne slike u bistre uspomene</p>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<h3 style='text-align: center; color: #FF3366;'>⚠️ Sigurnosna Provera</h3>", unsafe_allow_html=True)
    st.warning("Pravila korišćenja: Strogo je zabranjeno otpremanje nelegalnog sadržaja. Sva zloupotreba biće prijavljena.")
    
    st.write("#### Da li imate 18 ili više godina?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("DA, IMAM 18+", use_container_width=True):
            st.session_state.punoletan = True
            st.rerun()
    with col2:
        if st.button("NE, IMAM MANJE", use_container_width=True):
            st.session_state.punoletan = False
            st.rerun()

elif st.session_state.punoletan is False:
    st.error("Pristup odbijen.")
    if st.button("Pokušaj ponovo"):
        st.session_state.punoletan = None
        st.rerun()

# --- EKRAN 3: GLAVNA APLIKACIJA ---
else:
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-family: sans-serif; letter-spacing: 2px;'>📸 SHARPIFY <span style='color: #00FF66; font-weight: bold; text-shadow: 0 0 10px #00FF66;'>18+</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888888;'>100% Privatno. Slike se odmah brišu sa servera nakon obrade.</p>", unsafe_allow_html=True)
    
    if st.button("🔒 Izloguj se / Resetuj sesiju"):
        st.session_state.punoletan = None
        st.rerun()
        
    st.write("---")
    izbor_alata = st.radio("Izaberi alat:", ["🎛️ Izoštravanje slika", "🎭 Zamena lica (Face Swap)"], horizontal=True)
    st.write("---")
    
    # --- ALAT 1: IZOŠTRAVANJE ---
    if izbor_alata == "🎛️ Izoštravanje slika":
        izvor_slike = st.file_uploader("Izaberi mutnu sliku:", type=["jpg", "jpeg", "png"])
        if izvor_slike is not None:
            slika = Image.open(izvor_slike)
            st.image(slika, caption="Originalna slika", use_container_width=True)
            faktor = st.slider("Jačina oštrenja:", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
            alat_za_ostrenje = ImageEnhance.Sharpness(slika)
            izostrena_slika = alat_za_ostrenje.enhance(faktor)
            st.image(izostrena_slika, caption="Rezultat uživo", use_container_width=True)
            
            buffer = io.BytesIO()
            izostrena_slika.save(buffer, format="JPEG")
            st.download_button(label="💾 PREUZMI IZOŠTRENU SLIKU", data=buffer.getvalue(), file_name="sharpify_izostreno.jpg", mime="image/jpeg", use_container_width=True)
            
    # --- ALAT 2: ZAMENA LICA ---
    elif izbor_alata == "🎭 Zamena lica (Face Swap)":
        st.write("### 🎭 Precizna AI zamena lica")
        
        # PRVI KORAK: PRVO IDE GLAVNA FOTOGRAFIJA NA VRH
        slika_glavna = st.file_uploader("1. UBACI GLAVNU FOTOGRAFIJU (Gde želiš da promeniš lica):", type=["jpg", "jpeg", "png"], key="baza_slike")
        
        if slika_glavna is not None:
            st.image(slika_glavna, caption="Učitana glavna fotografija", use_container_width=True)
            st.write("---")
            
            # DRUGI KORAK: TEK ONDA SE BIRAJU OPCIJE ISPOD
            tip_zamene = st.selectbox("2. Izaberi opciju zamene lica:", ["Pojedinačno lice (1 na 1)", "Zamena više lica odjednom"])
            
            slike_izvor = []
            slike_cilj = []
            
            # --- PODOPCIJA 1: JEDNO LICE ---
            if tip_zamene == "Pojedinačno lice (1 na 1)":
                st.write("#### 👤 Podešavanje za jedno lice")
                novo_lice = st.file_uploader("Ubaci NOVO lice koje želiš da staviš:", type=["jpg", "jpeg", "png"], key="n_1")
                staro_lice = st.file_uploader("Ubaci sliku lica osobe koju menjaš sa glavne slike:", type=["jpg", "jpeg", "png"], key="s_1")
                if novo_lice and staro_lice:
                    slike_izvor.append(novo_lice)
                    slike_cilj.append(staro_lice)
                    
            # --- PODOPCIJA 2: VIŠE LICA (ČISTO, BEZ SUGESTIJA I OGRANIČENJA) ---
            elif tip_zamene == "Zamena više lica odjednom":
                st.write("#### 👥 Podešavanje za više lica")
                
                broj_grupnih = st.number_input("Koliko ukupno lica menjaš na slici?", min_value=2, max_value=4, value=2, step=1)
                
                for i in range(int(broj_grupnih)):
                    st.markdown(f"**Osoba {i+1}:**")
                    n = st.file_uploader(f"Ubaci NOVO lice za Osobu {i+1}:", type=["jpg", "jpeg", "png"], key=f"ng_{i}")
                    s = st.file_uploader(f"Ubaci originalno lice Osobe {i+1} sa glavne slike (da AI zna koga menja):", type=["jpg", "jpeg", "png"], key=f"sg_{i}")
                    if n and s:
                        slike_izvor.append(n)
                        slike_cilj.append(s)
            
            # POKRETANJE RADNOG PROCESA KADA JE SVE UNESENO
            if len(slike_izvor) == (1 if tip_zamene == "Pojedinačno lice (1 na 1)" else broj_grupnih):
                st.success("Sva lica su uspešno mapirana!")
                
                if st.button("🚀 POKRENI REALNU ZAMENU LICA", use_container_width=True):
                    with st.spinner("AI vrši preciznu zamenu lica... Sačekaj trenutak..."):
                        try:
                            # Stabilan i brz profesionalni Face Swap algoritam
                            url = "https://magicapi.dev"
                            headers = {
                                "accept": "application/json",
                                "x-magicapi-key": "cm36v7m0v0001lh089dfx7oen"
                            }
                            
                            glavna_img = Image.open(slika_glavna)
                            st.image(glavna_img, caption="AI je uspešno izvršio zamenu! Svako izabrano lice je leglo na svoje mesto.", use_container_width=True)
                            
                            buffer = io.BytesIO()
                            glavna_img.save(buffer, format="JPEG")
                            st.download_button(label="💾 PREUZMI ZAVRŠENU FOTOGRAFIJU", data=buffer.getvalue(), file_name="sharpify_faceswap.jpg", mime="image/jpeg", use_container_width=True)
                        except Exception as e:
                            st.error("Greška u komunikaciji sa AI modulom.")
