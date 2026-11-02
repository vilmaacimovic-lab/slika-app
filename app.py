
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io

# Podešavanje stranice
st.set_page_config(page_title="Sharpify AI - Professional Studio", layout="centered")

# Prikazivanje Adsterra baner reklame
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

# Popunder reklama
popunder_kod = """
ZALEPI_SVOJ_POPUNDER_KOD_OVDE
"""
components.html(popunder_kod, height=0, width=0)

# Naslov aplikacije (na engleskom)
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>SHARPEN <span style='color: #00FF66;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa; font-style: italic;'>Professional AI Studio. Upload up to 10 photos at once.</p>", unsafe_allow_html=True)

# Polje za preuzimanje slika
sve_slike = st.file_uploader("Choose or drop photos (Maximum 10 photos at once):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if sve_slike:
    if len(sve_slike) > 10:
        st.warning("⚠️ You selected more than 10 photos. The system will process the first 10 for optimal speed.")
        sve_slike = sve_slike[:10]

    st.success(f"Successfully loaded {len(sve_slike)} photos!")
    st.markdown("---")

    for brojac, pojedinacna_slika in enumerate(sve_slike):
        st.markdown(f"### Photo number {brojac + 1}: {pojedinacna_slika.name}")
        
        slika = Image.open(pojedinacna_slika)
        st.image(slika, caption="Original version", use_container_width=True)

        st.markdown("# THREE SLIDERS FOR EACH PHOTO - MAXIMUM CONTROL")
        faktor_ostrenja = st.slider(f"1. Sharpening strength:", min_value=1.0, max_value=5.0, value=2.0, step=0.1, key=f"ostrenje_{brojac}")
        faktor_boje = st.slider(f"2. Color and vibrancy (Saturation):", min_value=1.0, max_value=3.0, value=1.2, key=f"boja_{brojac}")
        faktor_kontrasta = st.slider(f"3. Depth contrast:", min_value=1.0, max_value=3.0, value=1.1, key=f"kontrast_{brojac}")

        izostrena_slika = slika

        st.image(izostrena_slika, caption="Live processed result", use_container_width=True)

        pufer = io.BytesIO()
        izostrena_slika.save(pufer, format="JPEG")
        
        st.download_button(
            label=f"DOWNLOAD PROCESSED PHOTO {brojac + 1}",
            data=pufer.getvalue(),
            file_name=f"sharpify_studio_{brojac + 1}.jpg",
            mime="image/jpeg",
            key=f"dugme_{brojac}"
        )
        st.markdown("<hr style='border-top: 2px crtkana #333;'>", unsafe_allow_html=True)
