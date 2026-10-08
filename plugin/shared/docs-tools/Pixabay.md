# Pixabay.com - Bibliothèque libre de droit

C'est l'API la plus permissive pour un agent. Contrairement aux autres, ses conditions d'utilisation t'autorisent explicitement à télécharger et sauvegarder physiquement les fichiers.
Limites : 100 requêtes par minute

- Variable `PIXABAY_API_KEY` dans *zsh*.

## Search Images

1. Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| `q`   | str  | A URL encoded search term. If omitted, all images are returned. This value may not exceed 100 characters. Example: "yellow+flower" |
| `image_type` | str | The type of image to search for. Valid values are `photo`, `illustration`, `vector`, and `all`. Default: `photo` |
| `orientation` | str | The orientation of the image. Valid values are `horizontal`, `vertical`, and `all`. Default: `all` |
| `category` | str | The category of the image. Valid values are `all`, `animals`, `backgrounds`, `fashion`, `nature`, `science`, `sports`, `technics`, and `transport`. Default: `all` |
| `colors` | str | The colors of the image. Valid values are `all`, `grayscale`, `transparent`, and `monochrome`. Default: `all` |
| `page` | int | The page number of the results to return. Default: `1` |
| `per_page` | int | The number of images to return per page. Valid values are 1-200. Default: `20` |

2. Requête

```python
import os
import requests

def search_and_download_image(query: str, dest_path: str = "image.jpg") -> str:
  # Récupération de la clé depuis l'environnement zsh
  api_key = os.getenv("PIXABAY_API_KEY")
  
  if not api_key:
      return "Erreur : La variable d'environnement PIXABAY_API_KEY introuvable."
      
  # 1. L'agent passe les mots-clés (idéalement en anglais)
  url = f"https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo"
  res = requests.get(url).json()
  
  if not res.get('hits'):
      return "Échec : aucune image trouvée."
      
  # 2. Récupération de l'URL de la première image
  image_url = res['hits'][0]['largeImageURL']
  
  # 3. Téléchargement et sauvegarde
  img_data = requests.get(image_url).content
  with open(dest_path, 'wb') as f:
      f.write(img_data)
      
  return f"Succès : image sauvegardée sous {dest_path}"
```

  3. Réponse

|Response key |	Description
| --- | --- |
|total |	The total number of hits.
|totalHits |	The number of images accessible through the API. By default, the API is limited to return a maximum of 500 images per query. |
|id |	A unique identifier for this image |
|pageURL |	Source page on Pixabay, which provides a download link for the original image of the dimension imageWidth x imageHeight and the file size imageSize |
|previewURL |	Low resolution images with a maximum width or height of 150 px (previewWidth x previewHeight) |
|webformatURL |	Medium sized image with a maximum width or height of 640 px (webformatWidth x webformatHeight) |
|largeImageURL |	Scaled image with a maximum width/height of 1280px |
|views |	Total number of views |
|downloads |	Total number of downloads |
|likes |	Total number of likes |
|comments |	Total number of comments |
|user_id, user |	User ID and name of the contributor. Profile URL: https://pixabay.com/users/{ USERNAME }-{ ID }/ |
|userImageURL |	Profile picture URL (250 x 250 px) |
