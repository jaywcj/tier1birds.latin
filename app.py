from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Bird data
birds = {
    "Javan myna": "Acridotheres javanicus",
    "Common myna": "Acridotheres tristis",
    "Common iora": "Aegithina tiphia",
    "White-breasted waterhen": "Amaurornis phoenicurus",
    "Oriental pied hornbill": "Anthracoceros albirostris",
    "Brown-throated sunbird": "Anthreptes malacensis",
    "Asian glossy starling": "Aplonis panayensis",
    "Olive-backed sunbird": "Cinnyris jugularis",
    "Rock dove": "Columba livia",
    "Oriental magpie-robin": "Copsychus saularis",
    "Large-billed crow": "Corvus macrorhynchos",
    "House crow": "Corvus splendens",
    "Scarlet-backed flowerpecker": "Dicaeum cruentatum",
    "Common flameback": "Dinopium javanense",
    "Asian koel": "Eudynamys scolopaceus",
    "Red junglefowl": "Gallus gallus",
    "Zebra dove": "Geopelia striata",
    "White-throated kingfisher": "Halcyon smyrnensis",
    "Scaly-breasted munia": "Lonchura punctulata",
    "Blue-tailed bee-eater": "Merops philippinus",
    "Blue-throated bee-eater": "Merops viridis",
    "Black-naped oriole": "Oriolus chinensis",
    "Common tailorbird": "Orthotomus sutorius",
    "Eurasian tree sparrow": "Passer montanus",
    "Yellow-vented bulbul": "Pycnonotus goiavier",
    "Spotted dove": "Spilopelia chinensis",
    "Collared kingfisher": "Todiramphus chloris",
    "Pink-necked green pigeon": "Treron vernans",
    "Sunda pygmy woodpecker": "Yungipicus moluccensis"
}

latin_to_common = {v: k for k, v in birds.items()}

# Etymology explanations for the Latin names
latin_name_etymology = {
    "Acridotheres javanicus": "Acridotheres means 'grasshopper hunter', from Greek akris (grasshopper) and theres (hunter), referring to its insect-eating habits. Javanicus refers to its origin in Java.",
    "Acridotheres tristis": "Acridotheres means 'grasshopper hunter', from Greek akris (grasshopper) and theres (hunter). Tristis means 'sad' in Latin, likely referring to the bird's melancholic call.",
    "Aegithina tiphia": "The genus name Aegithina is from Ancient Greek aigithos or aiginthos, a mythical bird mentioned by Aristotle and other classical authors. The etymology of specific epithet tiphia is uncertain.",
    "Amaurornis phoenicurus": "Amaurornis comes from Greek amauro (dark, obscure) and ornis (bird), meaning 'hidden bird'. Phoenicurus comes from Greek phoinix (crimson) and oura (tail), meaning 'red-tailed'.",
    "Anthracoceros albirostris": "Anthracoceros combines Greek anthrax (coal) and keros (horn), meaning 'black-horned'. Albirostris comes from Latin albus (white) and rostrum (bill), meaning 'white-billed'.",
    "Anthreptes malacensis": "Anthreptes is derived from Greek anthos (flower) and ereptes (snatcher), and is a genus of sunbirds. Malacensis refers to the bird's origin in Malaya.",
    "Aplonis panayensis": "Aplonis refers to a genus of starlings, with Greek haploos (simple) and oninos (bird). Panayensis denotes its habitat on the island of Panay in the Philippines.",
    "Cinnyris jugularis": "Cinnyris is Greek for 'sunbird'. Jugularis is Latin for 'throated', referring to the bird's distinctive throat color.",
    "Columba livia": "Columba is Latin for 'dove'. Livia is derived from Latin, meaning 'bluish', which refers to the bluish-grey coloration of the rock pigeon.",
    "Copsychus saularis": "Copsychus is from Greek kopsychos, meaning 'mimic', referring to its mimicking abilities. Saularis is a latinsation the Hindi word saulary which means a 'hundred songs'.",
    "Corvus macrorhynchos": "Corvus is Latin for 'crow'. Macrorhynchos is from Greek makros (large) and rhynchos (beak), meaning 'large-billed'.",
    "Corvus splendens": "Corvus means 'crow' in Latin. Splendens is Latin for 'shining', referring to the bird's glossy feathers.",
    "Dicaeum cruentatum": "Dicaeum refers to a genus of flowerpeckers, originating from the Greek dikaios (righteous). Cruentatum comes from Latin cruentus, meaning 'bloody', referring to the bird’s red color.",
    "Dinopium javanense": "Dinopium combines the Classical Greek deinos meaning 'mighty' and ōps/ōpos meaning 'appearance'. Javanense refers to its habitat in Java.",
    "Eudynamys scolopaceus": "Eudynamys combines Greek eu (good) and dynamis (power), meaning 'good power', likely referring to its loud calls. Scolopaceus is from Latin, referencing a resemblance to woodcocks.",
    "Gallus gallus": "Gallus is Latin for 'rooster'. Gallus also indicates the species, emphasizing the bird's identity as the typical rooster.",
    "Geopelia striata": "Geopelia combines Greek geo (earth) and peleia (dove), meaning 'ground dove'. Striata is Latin for 'striped', referring to the bird's streaked plumage.",
    "Halcyon smyrnensis": "Halcyon is Greek for 'kingfisher', from the mythological bird associated with calm seas. Smyrnensis refers to Smyrna, an ancient city in modern-day Turkey.",
    "Lonchura punctulata": "Lonchura is derived from Greek lonche (spear) and oura (tail), possibly referring to the bird’s tail shape. Punctulata comes from Latin punctum, meaning 'spotted'.",
    "Merops philippinus": "Merops is Greek for 'bee-eater', reflecting the bird's diet. Philippinus refers to the bird's presence in the Philippines.",
    "Merops viridis": "Merops means 'bee-eater' in Greek. Viridis is Latin for 'green', referring to the bird’s green plumage.",
    "Oriolus chinensis": "Oriolus is Latin for 'oriole', a bird noted for its golden-yellow color. Chinensis indicates its geographical link to China.",
    "Orthotomus sutorius": "Orthotomus is derived from Greek orthos (straight) and tomos (cutting), referring to the bird’s nest-building habit of 'tailoring' leaves. Sutorius is Latin for 'shoemaker', referencing its precise nest-building skills.",
    "Passer montanus": "Passer is Latin for 'sparrow'. Montanus means 'of the mountains' in Latin, referring to its habitat.",
    "Pycnonotus goiavier": "Pycnonotus is Greek for 'dense back', referring to the bird's compact form. Goiavier derives from a local name, indicating its range in the Philippines.",
    "Spilopelia chinensis": "Spilopelia combines Greek spilos (spot) and peleia (dove), meaning 'spotted dove'. Chinensis refers to China, where the species is found.",
    "Todiramphus chloris": "Todiramphus comes from Greek todis (kingfisher) and ramphos (beak), meaning 'sharp-beaked kingfisher'. Chloris is Greek for 'green', referring to the bird’s green plumage.",
    "Treron vernans": "Treron is Greek for 'pigeon'. Vernans comes from the Latin vernare, meaning 'to flourish or grow green', likely referencing the bird’s vibrant green feathers.",
    "Yungipicus moluccensis": "The genus name likely combines 'yung' meaning 'young' or 'small' and 'picus', which is Latin for 'woodpecker'. The Latin name Moluccas refers to an island group in Indonesia.",
}

@app.route('/')
def index():
    session['score'] = 0  # Initialize score
    session['question_count'] = 0  # Initialize question count
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    if session['question_count'] >= 10:
        return jsonify({'finished': True, 'score': session['score']})

    common_name, correct_latin = random.choice(list(birds.items()))
    options = generate_options(correct_latin)
    session['current_question'] = {
        'common_name': common_name,
        'correct_latin': correct_latin
    }
    session['question_count'] += 1
    return jsonify({
        'common_name': common_name,
        'options': options,
        'correct_latin': correct_latin
    })

def generate_options(correct_latin):
    incorrect_latin = random.sample([name for name in birds.values() if name != correct_latin], 2)
    options = [correct_latin] + incorrect_latin
    random.shuffle(options)
    return options

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    selected_latin = data['selected_latin']
    correct_latin = session['current_question']['correct_latin']
    common_name = session['current_question']['common_name']
    response = {}

    if selected_latin == correct_latin:
        session['score'] += 1  # Increment score
        etymology = latin_name_etymology.get(correct_latin, "")
        response['correct'] = True
        response['message'] = f"Correct! {etymology}"
    else:
        selected_common = latin_to_common[selected_latin]
        response['correct'] = False
        response['message'] = f"Wrong! \n '{selected_latin}' refers to the {selected_common}. \n The answer is '{correct_latin}'."

    return jsonify(response)

@app.route('/final_score')
def final_score():
    return jsonify({'score': session['score']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
