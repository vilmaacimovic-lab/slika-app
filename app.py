import streamlit as st
from PIL import Image, ImageEnhance
import io

# Cisto i profesionalno podesavanje za fotografe
st.set_page_config(page_title="Sharpify AI - Profesionalno Izoštravanje", page_icon="📸", layout="centered")

# Tvoja Adsterra reklama radi u pozadini i donosi lova od svakog klika na aplikaciju
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

# Moderan, diskretan tamni dizajn
st.markdown("""
    <style>
    .main { background-color: #0d0f12; }
    div.stButton > button:first-child {
        background-color: #00FF66;
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Naslov aplikacije - cist alat za fotografe i brzu obradu
st.markdown("<h1 style='text-align: center; color: #ffffff; font-family: sans-serif;'>📸 SHARPIFY <span style='color: #00FF66; font-weight: bold;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa; font-style: italic;'>Profesionalno AI izoštravanje fotografija u jednom kliku. Uštedite vreme bez Photoshopa.</p>", unsafe_allow_html=True)
st.write("---")

# Glavna i jedina funkcija na sajtu - upload mutne slike
izvor_slike = st.file_uploader("Izaberi mutnu fotografiju za instant izoštravanje:", type=["jpg", "jpeg", "png"])

if izvor_slike is not None:
    slika = Image.open(izvor_slike)
    st.image(slika, caption="Originalna fotografija", use_container_width=True)
    
    # Klizac za jacinu ostrine koji korisnik sam bira prstom na telefonu ili mišem
    faktor = st.slider("Podesi jačinu oštrenja:", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
    
    # AI motor koji obradjuje sliku u privremenoj memoriji servera
    alat_za_ostrenje = ImageEnhance.Sharpness(slika)
    izostrena_slika = alat_za_ostrenje.enhance(faktor)
    
    st.image(izostrena_slika, caption="Izoštren rezultat uživo", use_container_width=True)
    
    # Priprema za sigurno preuzimanje slike na uredjaj
    buffer = io.BytesIO()
    izostrena_slika.save(buffer, format="JPEG")
    
    st.download_button(
        label="💾 PREUZMI IZOŠTRENU SLIKU",
        data=buffer.getvalue(),
        file_name="sharpify_pro_izostreno.jpg",
        mime="image/jpeg",
        use_container_width=True
    )
