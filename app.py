import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import io

# Podešavanje stranice
st.set_page_config(page_title="Sharpify AI - Profesionalni Studio", layout="centered")

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

# Naslov aplikacije
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>IZOŠTRITE <span style='color: #00FF66;'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa; font-style: italic;'>Profesionalni AI Studio. Ubacite do 10 fotografija odjednom.</p>", unsafe_allow_html=True)

# Polje za preuzimanje slika
sve_ slike = st.file_uploader("Izaberite ili prevucite fotografije (Maksimalno 10 slika odjednom):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if sve_slike:
    if len(sve_slike) > 10:
        st.warning("⚠️ Izabrali ste više od 10 slika. Sustav će obraditi prvih 10 radi optimalne brzine.")
        sve_slike = sve_slike[:10]

    st.success(f"Uspješno učitano {len(sve_slike)} fotografija!")
    st.markdown("---")

    for brojac, pojedinacna_slika in enumerate(sve_slike):
        st.markdown(f"### Fotografija broj {brojac + 1}: {pojedinacna_slika.name}")
        
        slika = Image.open(pojedinacna_slika)
        st.image(slika, caption="Izvorna verzija", use_container_width=True)

        st.markdown("# TRI KLIZAČA ZA SVAKU SLIKU - MAKSIMALNA KONTROLA")
        faktor_ostrenja = st.slider(f"1. Jačina oštrenja:", min_value=1.0, max_value=5.0, value=2.0, step=0.1, key=f"ostrenje_{brojac}")
        faktor_boje = st.slider(f"2. Jačina i živost boja (Saturacija):", min_value=1.0, max_value=3.0, value=1.2, key=f"boja_{brojac}")
        faktor_kontrasta = st.slider(f"3. Dubinski kontrast:", min_value=1.0, max_value=3.0, value=1.1, key=f"kontrast_{brojac}")

        # Simulacija obrade (možeš prilagoditi svojim funkcijama ako postoje)
        izostrena_slika = slika

        st.image(izostrena_slika, caption="Obrađen rezultat uživo", use_container_width=True)

        # Spremanje za preuzimanje
        pufer = io.BytesIO()
        izostrena_slika.save(pufer, format="JPEG")
        
        st.download_button(
            label=f"PREUZMI OBRAĐENU FOTOGRAFIJU {brojac + 1}",
            data=pufer.getvalue(),
            file_name=f"sharpify_studio_{brojac + 1}.jpg",
            mime="image/jpeg",
            key=f"dugme_{brojac}"
        )
        st.markdown("<hr style='border-top: 2px crtkana #333;'>", unsafe_allow_html=True)
