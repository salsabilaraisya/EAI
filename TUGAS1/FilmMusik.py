import streamlit as st
import requests

# HTTP request ke IMDb
def search_imdb(query):
    url = "https://imdb146.p.rapidapi.com/v1/find/"
    querystring = {"query": query}
    headers = {
        "X-RapidAPI-Key": "27a8d90787msh4509e512529dc68p11ad92jsn3afde2993bee",
        "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# HTTP request ke Spotify
def search_spotify(query, access_token):
    url = "https://api.spotify.com/v1/search"
    querystring = {"q": query, "type": "track"}
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Mendapatkan access token dari Spotify
def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": "4f51cd9ac6d24ac397b18c7ed32f5258",
        "client_secret": "04c15d411ec74ed4a19fadd471126f3e"
    }
    auth_response = requests.post(auth_url, data=data)
    access_token = auth_response.json()["access_token"]
    return access_token


# Main function
def main():
    st.title("Aplikasi Pencarian Film dan Musik")

    # input user untuk pemilihan jenis film/musik
    jenis_pencarian = st.selectbox("Mau cari film atau cari musik nih?", ("Film", "Musik"))

    if jenis_pencarian == "Film":
        # input user
        query = st.text_input("Oke, film apa yang kamu cari? ")
        if st.button("Cari Film"):  
            if query:  
                # Cari di IMDb
                imdb_result = search_imdb(query)
                # Menampilkan hasil film
                if imdb_result.get("titleResults"):
                    title_results = imdb_result["titleResults"]["results"]
                    num_columns = 2  
                    for i in range(0, len(title_results), num_columns):
                        cols = st.columns(num_columns)  
                        for j in range(num_columns):
                            idx = i + j
                            if idx < len(title_results):
                                result = title_results[idx]
                                with cols[j]:  
                                    st.subheader(result["titleNameText"])
                                    st.write(f"Tahun Rilis: {result.get('titleReleaseText', 'Tidak tersedia')}")
                                    st.write(f"Pemain Utama: {', '.join(result.get('topCredits', ['Tidak tersedia']))}")
                                    st.image(result["titlePosterImageModel"]["url"], caption=result["titlePosterImageModel"]["caption"], width=250)  # Mengatur lebar gambar
                else:
                    st.write("Maaf, tidak ada film yang ditemukan.")
            else:
                st.write("Masukkan judul film untuk melakukan pencarian.")
    
    elif jenis_pencarian == "Musik":
        # Mendapatkan access token dari Spotify
        access_token = get_access_token()
        
        # input user
        query = st.text_input("Oke, lagu apa yang kamu cari? ")
        if st.button("Cari Lagu"):
            # Panggil fungsi pencarian di Spotify dengan access token
            spotify_result = search_spotify(query, access_token)
            # Menampilkan hasil pencarian spotify
            if "tracks" in spotify_result:
                tracks = spotify_result["tracks"]
                if tracks:
                    st.subheader("Daftar Lagu yang Ditemukan:")
                    for track in tracks["items"]:
                        st.write(f"- {track['name']} oleh {', '.join(artist['name'] for artist in track['artists'])}")
                else:
                    st.write("Maaf, tidak ada lagu yang ditemukan.")
            else:
                st.write("Maaf, tidak ada lagu yang ditemukan.")        
    else:
        st.write("Maaf, aku nggak ngerti itu. Coba lagi ya, film atau musik doang.")

if __name__ == "__main__":
    main()