import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageEnhance
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

# Naslov aplikacije
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>SHARPEN <span style='color: #00FF66;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa; font-style: italic;'>Professional AI Studio. Upload up to 10 photos at once.</p>", unsafe_allow_html=True)

# Polje za preuzimanje slika
sve_slike = st.file_uploader("Choose or drop photos (Maximum 10 photos at once):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if sve_slike:
    if len(sve_slike) > 10:
        st.warning("⚠️ You selected more than 10 photos. The system will process the first 10 for optimal speed.")
        sve_slike = sve_slike[:10]

    st.success(f"Successfully loaded {len(sve_slike)} photo(s)!")
    st.markdown("---")

    for brojac, pojedinacna_slika in enumerate(sve_slike):
        st.markdown(f"### Photo number {brojac + 1}: {pojedinacna_slika.name}")
        
        slika = Image.open(pojedinacna_slika).convert("RGB")
        
        # Opcije za rotaciju
        col_rot1, col_rot2 = st.columns(2)
        with col_rot1:
            rotiraj_levo = st.button(f"🔄 Rotate Left 90°", key=f"rot_left_{brojac}")
        with col_rot2:
            rotiraj_desno = st.button(f"🔄 Rotate Right 90°", key=f"rot_right_{brojac}")

        if f"rotacija_{brojac}" not in st.session_state:
            st.session_state[f"rotacija_{brojac}"] = 0

        if rotiraj_levo:
            st.session_state[f"rotacija_{brojac}"] = (st.session_state[f"rotacija_{brojac}"] + 90) % 360
        if rotiraj_desno:
            st.session_state[f"rotacija_{brojac}"] = (st.session_state[f"rotacija_{brojac}"] - 90) % 360

        if st.session_state[f"rotacija_{brojac}"] != 0:
            slika = slika.rotate(st.session_state[f"rotacija_{brojac}"], expand=True)

        st.image(slika, caption="Original photo", use_container_width=True)

        st.markdown("### ADJUSTMENT CONTROLS")
        faktor_ostrenja = st.slider("1. Sharpening strength:", min_value=1.0, max_value=5.0, value=2.0, step=0.1, key=f"ostrenje_{brojac}")
        faktor_boje = st.slider("2. Color and vibrancy (Saturation):", min_value=0.0, max_value=3.0, value=1.2, step=0.1, key=f"boja_{brojac}")
        faktor_kontrasta = st.slider("3. Depth contrast:", min_value=0.5, max_value=3.0, value=1.1, step=0.1, key=f"kontrast_{brojac}")
        faktor_osvetljenja = st.slider("4. Brightness:", min_value=0.5, max_value=2.0, value=1.0, step=0.1, key=f"osvetljenje_{brojac}")

        # Primena efekata uživo u RAM memoriji
        obradjena_slika = ImageEnhance.Sharpness(slika).enhance(faktor_ostrenja)
        obradjena_slika = ImageEnhance.Color(obradjena_slika).enhance(faktor_boje)
        obradjena_slika = ImageEnhance.Contrast(obradjena_slika).enhance(faktor_kontrasta)
        obradjena_slika = ImageEnhance.Brightness(obradjena_slika).enhance(faktor_osvetljenja)

        st.image(obradjena_slika, caption="Live processed result", use_container_width=True)

        pufer = io.BytesIO()
        obradjena_slika.save(pufer, format="JPEG", quality=95)
        
        st.download_button(
            label=f"DOWNLOAD PROCESSED PHOTO {brojac + 1}",
            data=pufer.getvalue(),
            file_name=f"sharpify_studio_{brojac + 1}.jpg",
            mime="image/jpeg",
            key=f"dugme_{brojac}"
        )
        st.markdown("<hr style='border-top: 2px dashed #333;'>", unsafe_allow_html=True)
