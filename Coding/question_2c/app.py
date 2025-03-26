from flask import Flask, jsonify, render_template
import requests
import pylhe
from particle import Particle

app = Flask(__name__)


events = None
event_index = 0
url = "https://www.ppe.gla.ac.uk/~abuckley/top.lhe"


# Processes the single event and builds a JSON
def parse_event_with_edges(event):
    particles = []
    edges = []

    for i, p in enumerate(event.particles):
        symbol = Particle.from_pdgid(p.id).name
        particles.append({
            "index": i,
            "px": p.px,
            "py": p.py,
            "pz": p.pz,
            "pdgId": p.id,
            "symbol": symbol
        })

        if p.mother1 > 0:
            edges.append({"from": p.mother1 - 1, "to": i})
        if p.mother2 > 0 and p.mother2 != p.mother1:
            edges.append({"from": p.mother2 - 1, "to": i})

    return {"particles": particles, "edges": edges}


# Serves the event endpoint
@app.route('/event')
def event():
    global events, event_index
    try:
        event = next(events)
        event_details = parse_event_with_edges(event)
        event_index += 1
        return jsonify(event_details)
    except StopIteration:
        return jsonify({"error": "No more events."}), 404


# Actual home route
@app.route('/')
def index():
    global events
    response = requests.get(url)

    with open("data.lhe", mode="wb") as file:
        file.write(response.content)

    events = pylhe.read_lhe_with_attributes("data.lhe")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
