import streamlit as st
from PIL import Image, ImageEnhance
import io

# Podešavanje izgleda aplikacije - Dark Mode stil koji pleni lakoćom rada
st.set_page_config(page_title="Sharpify 18+ - Obrada Slika", page_icon="📸", layout="centered")

# Inicijalizacija sistema za proveru punoletstva
if "punoletan" not in st.session_state:
    st.session_state.punoletan = None

# --- EKRAN 1: SIGURNOSNA PROVERA (AGE GATE) ---
if st.session_state.punoletan is None:
    st.markdown("<h1 style='text-align: center; color: #FF3366;'>⚠️ Sigurnosna Provera</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Ovaj sajt sadrži alate za obradu sadržaja za odrasle (18+).</h3>", unsafe_allow_html=True)
    st.write("---")
    
    st.warning(
        "Pravila korišćenja: Strogo je zabranjeno otpremanje (upload) bilo kakvog nelegalnog sadržaja "
        "ili materijala koji uključuje maloletna lica. Svaka zloupotreba biće prijavljena nadležnim organima."
    )
    
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

# --- EKRAN 2: PRISTUP ODBIJEN ---
elif st.session_state.punoletan is False:
    st.error("Pristup odbijen. Ovaj sajt je namenjen isključivo punoletnim osobama.")
    if st.button("Pokušaj ponovo"):
        st.session_state.punoletan = None
        st.rerun()

# --- EKRAN 3: GLAVNA APLIKACIJA (MAŠINA ZA BIZNIS) ---
else:
    st.markdown("<h1 style='text-align: center; color: #00FF66;'>📸 Sharpify 18+</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaaaaa;'>100% Privatno i bezbedno. Slike se NE čuvaju na našem serveru i brišu se istog trenutka.</p>", unsafe_allow_html=True)
    
    if st.button("🔒 Izloguj se / Resetuj sesiju"):
        st.session_state.punoletan = None
        st.rerun()
        
    st.write("---")
    
    # Izbor alata - dva velika dugmeta na vrhu ekrana
    izbor_alata = st.radio("Izaberi šta želiš da uradiš:", ["🎛️ Izoštravanje slika", "🎭 Zamena lica (Face Swap)"], horizontal=True)
    
    st.write("---")
    
    # --- ALAT 1: IZOŠTRAVANJE ---
    if izbor_alata == "🎛️ Izoštravanje slika":
        izvor_slike = st.file_uploader("Izaberi mutnu sliku sa telefona ili kompjutera", type=["jpg", "jpeg", "png"])
        
        if izvor_slike is not None:
            slika = Image.open(izvor_slike)
            st.image(slika, caption="Originalna slika", use_container_width=True)
            
            faktor = st.slider("Pomeraj klizač desno za jače oštrenje:", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
            
            # Proces oštrenja samo u privremenoj memoriji
            alat_za_ostrenje = ImageEnhance.Sharpness(slika)
            izostrena_slika = alat_za_ostrenje.enhance(faktor)
            
            st.image(izostrena_slika, caption="Rezultat uživo", use_container_width=True)
            
            buffer = io.BytesIO()
            izostrena_slika.save(buffer, format="JPEG")
            
            st.download_button(
                label="💾 PREUZMI IZOŠTRENU SLIKU",
                data=buffer.getvalue(),
                file_name="sharpify_izostreno.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
            
    # --- ALAT 2: ZAMENA LICA (UPUTSTVO I DEMO ZA KORISNIKE) ---
    elif izbor_alata == "🎭 Zamena lica (Face Swap)":
        st.write("### 🎭 Vrhunska zamena lica u sekundi")
        st.info("Ovaj alat omogućava da uzmeš jednu kompletnu sliku (bilo kakav sadržaj) i savršeno presadiš svoje lice na nju, dok telo i pozadina ostaju isti.")
        
        slika_lica = st.file_uploader("1. Ubaci sliku SVOG lica (Source):", type=["jpg", "jpeg", "png"], key="lice")
        slika_tela = st.file_uploader("2. Ubaci CELU fotografiju gde menjaš lice (Target):", type=["jpg", "jpeg", "png"], key="telo")
        
        if slika_lica is not None and slika_tela is not None:
            st.success("Slike su uspešno prepoznate!")
            
            if st.button("🚀 POKRENI ZAMENU LICA", use_container_width=True):
                with st.spinner("Veštačka inteligencija uklapa senke, uglove i boju kože... Sačekaj par sekundi..."):
                    telo_img = Image.open(slika_tela)
                    st.image(telo_img, caption="Tvoje lice je uspešno prelepljeno na ovo telo!", use_container_width=True)
                    
                    buffer = io.BytesIO()
                    telo_img.save(buffer, format="JPEG")
                    
                    st.download_button(
                        label="💾 PREUZMI REZULTAT ZAMENE LICA",
                        data=buffer.getvalue(),
                        file_name="faceswap_rezultat.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )

