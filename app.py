from flask import Flask, render_template, Response, request
import requests
import os

app = Flask(__name__)
    
anime_list = {
"Takamine": {
"ep1": "https://krakenfiles.com/embed-video/vi8BYoKIWb",
"ep2": "https://krakenfiles.com/embed-video/LXezbPfTxg",
"title": "Haite Kudasai, Takamine-san",
"image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUW6z5r8HD_ruxH7uWwNdqtDI81N8SX_86Lrj295CxEblNWd10agAgiwJz&s=10",
"jenis": "Anime"
},
"Chi": {
"ep1": "https://krakenfiles.com/embed-video/V7vpmu44C6",
"ep2": "https://krakenfiles.com/embed-video/jJGnqKEjbj",
"ep3": "https://krakenfiles.com/embed-video/aLGjlnFiTE",
"ep4": "https://krakenfiles.com/embed-video/soQE7B6Cnp",
"ep5": "https://krakenfiles.com/embed-video/tNkbrgEkUQ",
"ep6": "https://krakenfiles.com/embed-video/eMgRL4iIxj",
"ep7": "https://krakenfiles.com/embed-video/OL32UlVfzg",
"title": "Chi. Chikyuu no Undou ni Tsuite",
"image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4rfvuYKE8plRGbyagXQd2xdK7hmTU_atslbKg4i81yw&s",
"jenis": "Anime"
},
"Hametsu": {
"ep1": "https://krakenfiles.com/embed-video/CwPt6UayS8",
"title": "Hametsu no Yuuwaku",
"image": "https://lk-21.icu/wp-content/uploads/2025/04/poster-1-170x255.jpg",
"jenis": "Anime2"
},
"Immoralroutine": {
"ep1": "https://krakenfiles.com/embed-video/2BZV8anzzP",
"title": "Immoral Routine",
"image": "https://admin.hentaini.com/uploads/Immoral_Routine_The_Animation_cover_e120d6f4e3.jpeg",
"jenis": "Anime2"
}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    filter_type = request.args.get('jenis', None)  # Get filter type from query parameters

    if filter_type:  # Filter by 'jenis' if specified
        filtered_anime = {key: value for key, value in anime_list.items() if value.get('jenis') == filter_type}
    else:  # If no filter selected, show empty list
        filtered_anime = {}

    return render_template('index.html', anime_list=filtered_anime, filter_type=filter_type)

@app.route('/anime/<id>', methods=['GET', 'POST'])
def anime(id):
    global video_url
    video_url = request.form.get('ep')
    anime = anime_list.get(id)

    current_ep = None
    if video_url and anime:
        for key, value in anime.items():
            if value == video_url and key.startswith('ep'):
                current_ep = key
                break
    try:
        if video_url is None or not video_url.startswith(('http://', 'https://')):
            raise requests.exceptions.MissingSchema("Invalid URL")
        
        return render_template('anime.html', show_iframe=True, anime=anime, id=id, current_ep=current_ep)

    except requests.exceptions.MissingSchema:
        return render_template('anime.html', show_iframe=False, anime=anime, id=id, current_ep=current_ep)    
    if not anime:
        return "Anime tidak ditemukan", 404        

@app.route('/embed_video', methods=['GET', 'POST'])
def embed_video():

    response = requests.get(video_url, stream=True)
    return Response(response.iter_content(chunk_size=1024),
                    content_type=response.headers['Content-Type'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)