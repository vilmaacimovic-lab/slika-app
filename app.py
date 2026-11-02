import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageEnhance
import io

# Cisto i profesionalno podesavanje za fotografe
st.set_page_config(page_title="Sharpify AI - Profesionalni Studio", page_icon="📸", layout="centered")
"""
# Prikazivanje Adsterra reklame
ad_html = """
<script type="text/javascript">
	atOptions = {
		'key' : 'fdf9ccaee046fb017df8b64eeb2c0b6b',
		'format' : 'iframe',
		'height' : 250,
		'width' : 300,
		'params' : {}
	};
</script>
<script type="text/javascript" src="//www.highperformantformat.com/fdf9ccaee046fb017df8b64eeb2c0b6b/invoke.js"></script>
"""
components.html(ad_html, height=270, width=320)
# Zvanična Streamlit funkcija koja gura reklamu na ekran telefona bez cenzure
components.html(kod_za_reklamu, height=260, scrolling=False)


# Naslov aplikacije - brz alat za grupnu obradu fotografa
st.markdown("<h1 style='text-align: center; color: #ffffff; font-family: sans-serif;'>📸 SHARPIFY <span style='color: #00FF66; font-weight: bold;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa; font-style: italic;'>Profesionalni AI Studio. Ubacite do 10 fotografija odjednom. Podesite oštrinu, jarke boje i savršen kontrast u par sekundi.</p>", unsafe_allow_html=True)
st.write("---")

# Polje koje prihvata vise slika odjednom
sve_slike = st.file_uploader("Izaberite ili prevucite fotografije (Maksimalno 10 slika odjednom):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if sve_slike:
    if len(sve_slike) > 10:
        st.warning("⚠️ Izabrali ste više od 10 slika. Sistem će obraditi prvih 10 radi optimalne brzine.")
        sve_slike = sve_slike[:10]
        
    st.success(f"Uspešno učitano {len(sve_slike)} fotografija!")
    st.write("---")
    
    # Prolazimo kroz svaku ubacenu sliku posebno
    for brojac, pojedinacna_slika in enumerate(sve_slike):
        st.markdown(f"### 🖼️ Fotografija broj {brojac + 1}: *{pojedinacna_slika.name}*")
        
        slika = Image.open(pojedinacna_slika)
        st.image(slika, caption="Originalna verzija", use_container_width=True)
        
        # TRI KLIZAČA ZA SVAKU SLIKU - MAKSIMALNA KONTROLA
        faktor_ostrenja = st.slider("1. Jačina oštrenja:", min_value=1.0, max_value=5.0, value=2.0, step=0.1, key=f"ostrenje_{brojac}")
        faktor_boje = st.slider("2. Jačina i živost boja (Saturacija):", min_value=1.0, max_value=3.0, value=1.2, step=0.1, key=f"boja_{brojac}")
        faktor_kontrasta = st.slider("3. Dubina kontrasta:", min_value=1.0, max_value=3.0, value=1.1, step=0.1, key=f"kontrast_{brojac}")
        
        # 1. KORAK: Oštrenje
        alat_za_ostrenje = ImageEnhance.Sharpness(slika)
        privremena_slika = alat_za_ostrenje.enhance(faktor_ostrenja)
        
        # 2. KORAK: Boje (Saturacija)
        alat_za_boje = ImageEnhance.Color(privremena_slika)
        privremena_slika = alat_za_boje.enhance(faktor_boje)
        
        # 3. KORAK: Kontrast
        alat_za_kontrast = ImageEnhance.Contrast(privremena_slika)
        izostrena_slika = alat_za_kontrast.enhance(faktor_kontrasta)
        
        st.image(izostrena_slika, caption="Obrađen rezultat uživo", use_container_width=True)
        
        # Spremanje za download
        buffer = io.BytesIO()
        izostrena_slika.save(buffer, format="JPEG")
        
        st.download_button(
            label=f"💾 PREUZMI OBRAĐENU FOTOGRAFIJU {brojac + 1}",
            data=buffer.getvalue(),
            file_name=f"sharpify_studio_{brojac + 1}.jpg",
            mime="image/jpeg",
            key=f"dugme_{brojac}",
            use_container_width=True
        )
        st.markdown("<br><hr style='border-top: 2px dashed #333;'><br>", unsafe_allow_html=True)
