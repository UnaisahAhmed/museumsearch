from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify, redirect, url_for
import re
import json
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Initialize an in-memory data structure for museums
museums = {} 


data = {
"1": {
    "id": "1",
    "title": "The Metropolitan Museum of Art",
    "image": "https://engage.metmuseum.org/media/f14c3uuo/assets__ga__locations__met-fifth-ave.jpg?anchor=center&mode=crop&quality=80&width=600&height=400&rnd=132599299305800000",
    "year": "1870",
    "summary": "The Met is one of the largest and most prestigious art museums in the world, housing over 2 million works of art from various cultures and time periods.",
    "director": ["Max Hollein"],
    "budget": "Pay-as-you-wish. Free for Columbia students.",
    "features": ["Ancient Art", "European Paintings", "American Art"],
    "score": "9.3",
    "genres": ["Art", "History", "Culture"],
    "similar museum ids": ["2", "3", "4"]
},
"2": {
    "id": "2",
    "title": "The Museum of Modern Art",
    "image": "https://www.moma.org/assets/visit/entrance-image--museum-crop-7516b01003659172f2d9dbc7a6c2e9d9.jpg",
    "year": "1929",
    "summary": "MoMA is a globally recognized museum dedicated to modern and contemporary art, with collections ranging from painting and sculpture to film and design.",
    "director": ["Glenn D. Lowry"],
    "budget": "Free for Columbia students",
    "features": ["Pablo Picasso", "Vincent van Gogh", "Andy Warhol"],
    "score": "9.0",
    "genres": ["Modern Art", "Contemporary", "Design"],
    "similar museum ids": ["1", "3", "5"]
},
"3": {
    "id": "3",
    "title": "The Solomon R. Guggenheim Museum",
    "image": "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/241000/241099-Guggenheim-Museum.jpg",
    "year": "1939",
    "summary": "Designed by Frank Lloyd Wright, the Guggenheim is a modern art museum known for its unique spiral architecture and groundbreaking exhibits.",
    "director": ["Richard Armstrong"],
    "budget": "Students $19",
    "features": ["Abstract Art", "Impressionism", "Expressionism"],
    "score": "8.9",
    "genres": ["Modern Art", "Architecture", "Exhibitions"],
    "similar museum ids": ["1", "4", "6"]
},
"4": {
    "id": "4",
    "title": "The American Museum of Natural History",
    "image": "https://scontent-lga3-3.xx.fbcdn.net/v/t39.30808-6/476225385_1186224253072160_6783304475927194980_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=cc71e4&_nc_ohc=5QnkFfilOL8Q7kNvgFXT0T9&_nc_oc=Adg2QSVBxAUFwSXklRXRB5vphpPU2EhXUkxTWCEQmNEtG2O4sxUJpT-gxA94x35gwzw&_nc_zt=23&_nc_ht=scontent-lga3-3.xx&_nc_gid=AnINpqRp1Kl_dVYAUYh7pVm&oh=00_AYCduFWz4MX4avx4qL-rEaNczVowvORfP8DShtSl--tMmw&oe=67CE1D1B",
    "year": "1869",
    "summary": "Known for its extensive collections in anthropology, biology, and earth sciences, the AMNH is one of the largest natural history museums in the world.",
    "director": ["Ellen V. Futter"],
    "budget": "Free for Columbia students",
    "features": ["Dinosaurs", "Human Evolution", "Space"],
    "score": "9.2",
    "genres": ["Natural History", "Science", "Education"],
    "similar museum ids": ["2", "3", "5"]
},
"5": {
    "id": "5",
    "title": "The Whitney Museum of American Art",
    "image": "https://whitneymedia.org/assets/image/827430/large_large_658.049c.jpg",
    "year": "1931",
    "summary": "The Whitney focuses on 20th- and 21st-century American art, offering a platform for living artists and emerging art forms.",
    "director": ["Adam D. Weinberg"],
    "budget": "The Whitney Museum now offers free admission to all visitors 25 years of age and younger.",
    "features": ["Edward Hopper", "Georgia O'Keeffe", "Jeff Koons"],
    "score": "8.8",
    "genres": ["American Art", "Contemporary", "Sculpture"],
    "similar museum ids": ["1", "2", "6"]
},
"6": {
    "id": "6",
    "title": "The Frick Collection",
    "image": "https://www.untappedcities.com/content/images/wp-content/uploads/2019/07/frick-collection-garden-court-john-russell-pope-nyc-1.jpg",
    "year": "1935",
    "summary": "A museum with a focus on Old Master paintings and European sculptures, housed in the former mansion of industrialist Henry Clay Frick.",
    "director": ["Ian Wardropper"],
    "budget": "Pay-as-you-wish",
    "features": ["Rembrandt", "Vermeer", "Goya"],
    "score": "9.0",
    "genres": ["Old Masters", "European Art", "Sculpture"],
    "similar museum ids": ["2", "3", "5"]
},
"7": {
    "id": "7",
    "title": "The New York Public Library",
    "image": "https://upload.wikimedia.org/wikipedia/commons/e/ee/New_York_Public_Library_-_Main_Branch_%2851396225599%29.jpg",
    "year": "1895",
    "summary": "A major research library and a cultural institution, known for its vast collections and iconic architecture, including the famous lion statues.",
    "director": ["Tony Marx"],
    "budget": "Free for Columbia students",
    "features": ["Books", "Archives", "Public Programs"],
    "score": "8.6",
    "genres": ["Literature", "History", "Education"],
    "similar museum ids": ["6", "4", "5"]
},
"8": {
    "id": "8",
    "title": "The Museum at the Fashion Institute of Technology",
    "image": "https://www.fitnyc.edu/museum/images/home-online-collections-2.jpg",
    "year": "1969",
    "summary": "Located at the Fashion Institute of Technology, this museum focuses on the history of fashion and design, showcasing both contemporary and historical collections.",
    "director": ["Dr. Valerie Steele"],
    "budget": "Free for Columbia students",
    "features": ["Fashion", "Design", "Textiles"],
    "score": "8.4",
    "genres": ["Fashion", "Design", "Textile Arts"],
    "similar museum ids": ["3", "7", "10"]
},

"9": {
    "id": "9",
    "title": "The Morgan Library & Museum",
    "image": "https://www.themorgan.org/sites/default/files/slider-image/Pierpont-Morgans-Library-bs.jpg",
    "year": "1906",
    "summary": "A breathtaking library and museum featuring rare manuscripts, historical documents, and fine art, originally founded by financier J.P. Morgan.",
    "director": ["Colin B. Bailey"],
    "budget": "College students can gain free admission to the Morgan Library & Museum on the first Sunday of each month!",
    "features": ["Manuscripts", "Rare Books", "Historical Art"],
    "score": "9.2",
    "genres": ["Art", "Literature", "History"],
    "similar museum ids": ["3", "6", "8"]
}, 

"10": {
    "id": "10",
    "title": "The Brooklyn Museum",
    "image": "https://cms-images.brooklynmuseum.org/bd6f71c54c1e211efd8cb797dfc546b6aa60bc11-8256x5504.jpg?w=2048&q=75",
    "year": "1895",
    "summary": "This museum offers an incredible mix of ancient and contemporary art, housing diverse collections in art, archaeology, and design.",
    "director": ["Anne Pasternak"],
    "budget": "$14 for students ages 20 and up who have a valid ID",
    "features": ["Egyptian Art", "Contemporary Art", "American Art"],
    "score": "8.7",
    "genres": ["Art", "Archaeology", "Design"],
    "similar museum ids": ["1", "8", "9"]
} 
}

@app.route('/')
def homepage():
    # three popular items dynamically
    popular_items = list(data.values())[:3]
    return render_template('index.html', popular_items=popular_items)


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search', '')
    
    # If the search term is empty or just whitespace
    if not search_term.strip():
        return redirect(request.referrer)  # Keep on the same page, no change
    
    # Search in multiple fields: title, genres, and features
    results = []
    for item_id, item in data.items():
        # Check for matches in title (assuming it's a string)
        title_match = search_term.lower() in item.get('title', '').lower()
        
        # Check for matches in genres (could be a list or string)
        genres_match = False
        genres = item.get('genres', [])
        if isinstance(genres, str):
            genres_match = search_term.lower() in genres.lower()
        elif isinstance(genres, list):
            # Check each genre in the list
            genres_match = any(search_term.lower() in genre.lower() for genre in genres if isinstance(genre, str))
        
        # Check for matches in features (could be a list or string)
        features_match = False
        features = item.get('features', [])
        if isinstance(features, str):
            features_match = search_term.lower() in features.lower()
        elif isinstance(features, list):
            # Check each feature in the list
            features_match = any(search_term.lower() in feature.lower() for feature in features if isinstance(feature, str))
        
        # If any field matches, include this item in results
        if title_match or genres_match or features_match:
            # Create a copy of the item with highlighted matches
            result_item = item.copy()
            result_item['id'] = item_id  # Make sure ID is included
            
            # Highlight matching text in title
            if title_match:
                result_item['title_highlighted'] = highlight_match(item.get('title', ''), search_term)
            else:
                result_item['title_highlighted'] = item.get('title', '')
                
            # Handle genres highlighting (could be a list or string)
            genres = item.get('genres', [])
            if isinstance(genres, str):
                if genres_match:
                    result_item['genres_highlighted'] = highlight_match(genres, search_term)
                else:
                    result_item['genres_highlighted'] = genres
            elif isinstance(genres, list):
                # Highlight each matching genre
                highlighted_genres = []
                for genre in genres:
                    if isinstance(genre, str) and search_term.lower() in genre.lower():
                        highlighted_genres.append(highlight_match(genre, search_term))
                    else:
                        highlighted_genres.append(genre)
                result_item['genres_highlighted'] = highlighted_genres
            
            # Handle features highlighting (could be a list or string)
            features = item.get('features', [])
            if isinstance(features, str):
                if features_match:
                    result_item['features_highlighted'] = highlight_match(features, search_term)
                else:
                    result_item['features_highlighted'] = features
            elif isinstance(features, list):
                # Highlight each matching feature
                highlighted_features = []
                for feature in features:
                    if isinstance(feature, str) and search_term.lower() in feature.lower():
                        highlighted_features.append(highlight_match(feature, search_term))
                    else:
                        highlighted_features.append(feature)
                result_item['features_highlighted'] = highlighted_features
                
            results.append(result_item)
    
    return render_template('search_results.html', results=results, search_term=search_term)

def highlight_match(text, search_term):
    """Highlight the search term in the text by wrapping it in a span with a highlight class"""
    import re
    pattern = re.compile(f'({re.escape(search_term)})', re.IGNORECASE)
    return pattern.sub(r'<span class="search-highlight">\1</span>', text)



@app.route('/add', methods=['GET', 'POST'])
def add_museum():
    if request.method == 'POST':
        # Collect form data
        title = request.form['title'].strip()
        image = request.form['image'].strip()
        year = request.form['year'].strip()
        summary = request.form['summary'].strip()
        director = request.form['director'].strip()
        budget = request.form['budget'].strip()
        features = request.form['features'].strip()
        score = request.form['score'].strip()
        genres = request.form['genres'].strip()
        similar_ids = request.form['similar_ids'].strip()

        # Validation
        errors = False
        error_messages = []

        if not title:
            error_messages.append("Title is required.")
            errors = True
        if not image:
            error_messages.append("Image URL is required.")
            errors = True
        if not year.isdigit():
            error_messages.append("Year must be a number.")
            errors = True
        if not summary:
            error_messages.append("Summary is required.")
            errors = True
        if not director:
            error_messages.append("Director(s) is/are required.")
            errors = True
        if not budget:
            error_messages.append("Budget/Entry Fee is required.")
            errors = True
        if not features:
            error_messages.append("Features are required.")
            errors = True
        if not score.replace('.', '', 1).isdigit():
            error_messages.append("Score must be a valid number.")
            errors = True
        if not genres:
            error_messages.append("Genres are required.")
            errors = True
        if not similar_ids:
            error_messages.append("Similar Museum IDs are required.")
            errors = True

        # If there are no errors, add the museum to the list
        if not errors:
            museum_id = str(len(museums) + 1)  # Create a new ID for the museum
            museums[museum_id] = {
                "id": museum_id,
                "title": title,
                "image": image,
                "year": year,
                "summary": summary,
                "director": director.split(','),
                "budget": budget,
                "features": features.split(','),
                "score": score,
                "genres": genres.split(','),
                "similar museum ids": similar_ids.split(',')
            }

            # Respond with JSON to indicate success and send the new item ID
            return jsonify({
                'success': True,
                'museum_id': museum_id,  # Send the museum_id back in the response
                'message': 'New item successfully created.'
            })

        # If errors, return them in the response
        return jsonify({'success': False, 'errors': error_messages})

    return render_template('add.html')

@app.route('/view/<museum_id>')
def view_item(museum_id):
    # First check the museums dictionary (user-added museums)
    item = museums.get(museum_id)
    
    # If not found there, check the data dictionary (pre-populated museums)
    if not item:
        item = data.get(museum_id)
    
    if not item:
        # If the item is not found in either dictionary, return a 404 error
        return "Museum not found", 404
    
    # Render the template and pass the museum data to it
    return render_template('view_item.html', item=item)

@app.route('/edit/<museum_id>', methods=['GET', 'POST'])
def edit_museum(museum_id):
    # Try to find the museum in both dictionaries
    item = museums.get(museum_id)
    
    if not item:
        item = data.get(museum_id)
    
    if not item:
        return "Museum not found", 404
    
    if request.method == 'POST':
        # Collect form data
        title = request.form['title'].strip()
        image = request.form['image'].strip()
        year = request.form['year'].strip()
        summary = request.form['summary'].strip()
        director = request.form['director'].strip()
        budget = request.form['budget'].strip()
        features = request.form['features'].strip()
        score = request.form['score'].strip()
        genres = request.form['genres'].strip()
        similar_ids = request.form['similar_ids'].strip()

        # Validation
        errors = False
        error_messages = []

        if not title:
            error_messages.append("Title is required.")
            errors = True
        if not image:
            error_messages.append("Image URL is required.")
            errors = True
        if not year.isdigit():
            error_messages.append("Year must be a number.")
            errors = True
        if not summary:
            error_messages.append("Summary is required.")
            errors = True
        if not director:
            error_messages.append("Director(s) is/are required.")
            errors = True
        if not budget:
            error_messages.append("Budget/Entry Fee is required.")
            errors = True
        if not features:
            error_messages.append("Features are required.")
            errors = True
        if not score.replace('.', '', 1).isdigit():
            error_messages.append("Score must be a valid number.")
            errors = True
        if not genres:
            error_messages.append("Genres are required.")
            errors = True
        if not similar_ids:
            error_messages.append("Similar Museum IDs are required.")
            errors = True

        # If there are no errors, update the museum
        if not errors:
            # Create updated museum object
            updated_museum = {
                "id": museum_id,
                "title": title,
                "image": image,
                "year": year,
                "summary": summary,
                "director": director.split(','),
                "budget": budget,
                "features": features.split(','),
                "score": score,
                "genres": genres.split(','),
                "similar museum ids": similar_ids.split(',')
            }
            
            # Update the proper dictionary
            if museum_id in museums:
                museums[museum_id] = updated_museum
            else:
                data[museum_id] = updated_museum
            
            # Redirect to the view page of the updated museum
            return redirect(url_for('view_item', museum_id=museum_id))
        
        # If errors, return them in the response
        return render_template('edit.html', item=item, errors=error_messages)
        
    # For GET request, render the edit form
    return render_template('edit.html', item=item)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

