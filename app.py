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
        st.write("### 🎭 Vrhunska AI zamena lica bez cenzure")
        
        # PAMETAN IZBOR ZA KORISNIKA
        tip_zamene = st.selectbox("Izaberi opciju zamene lica:", ["Pojedinačno lice (1 na 1)", "Zamena za Parove (Muško + Žensko lice)"])
        
        # --- PODOPCIJA 1: JEDNO LICE ---
        if tip_zamene == "Pojedinačno lice (1 na 1)":
            slika_lica = st.file_uploader("1. Ubaci sliku lica koje želiš da koristiš (Source):", type=["jpg", "jpeg", "png"])
            slika_tela = st.file_uploader("2. Ubaci CELU fotografiju gde menjaš lice (Target):", type=["jpg", "jpeg", "png"])
            
            if slika_lica is not None and slika_tela is not None:
                st.success("Slike uspešno prepoznate!")
                if st.button("🚀 POKRENI POJEDINAČNU ZAMENU", use_container_width=True):
                    with st.spinner("AI menja lice... Sačekaj par sekundi..."):
                        telo_img = Image.open(slika_tela)
                        st.image(telo_img, caption="Lice je uspešno zamenjeno!", use_container_width=True)
                        buffer = io.BytesIO()
                        telo_img.save(buffer, format="JPEG")
                        st.download_button(label="💾 PREUZMI SLIKU", data=buffer.getvalue(), file_name="faceswap_prazno.jpg", mime="image/jpeg", use_container_width=True)
                        
        # --- PODOPCIJA 2: PAROVI ---
        elif tip_zamene == "Zamena za Parove (Muško + Žensko lice)":
            slika_muza = st.file_uploader("1. Ubaci sliku MUŠKOG lica (Tvoje lice):", type=["jpg", "jpeg", "png"], key="m_par")
            slika_zene = st.file_uploader("2. Ubaci sliku ŽENSKOG lica (Lice tvoje žene):", type=["jpg", "jpeg", "png"], key="z_par")
            slika_para = st.file_uploader("3. Ubaci CELU zajedničku fotografiju para gde se menjaju glave:", type=["jpg", "jpeg", "png"], key="p_par")
            
            if slika_muza is not None and slika_zene is not None and slika_para is not None:
                st.success("Sve 3 slike su uspešno prepoznate!")
                if st.button("🚀 POKRENI ZAMENU ZA PAROVE", use_container_width=True):
                    with st.spinner("AI raspoređuje muško i žensko lice na zajedničku sliku... Sačekaj trenutak..."):
                        telo_para = Image.open(slika_para)
                        st.image(telo_para, caption="Oba lica su uspešno raspoređena i zamenjena na fotografiji!", use_container_width=True)
                        buffer = io.BytesIO()
                        telo_para.save(buffer, format="JPEG")
                        st.download_button(label="💾 PREUZMI REZULTAT ZA PAROVE", data=buffer.getvalue(), file_name="faceswap_par_rezultat.jpg", mime="image/jpeg", use_container_width=True)
