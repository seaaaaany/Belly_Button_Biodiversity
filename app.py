
# import relevant libraries
from flask import Flask, render_template, url_for, jsonify
import json

# python modules created for apis
from ORM_Queries import getSampleNames, getOTUbySamples, getSampleMetaData, getWashingFreq
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd


app = Flask(__name__)


# dashboard homepage
@app.route('/')
def hello():
    # Return the dashboard homepage.
    return render_template('index.html')


@app.route("/names")
def sampleNames():
    sampleNames = getSampleNames()
    return json.dumps(sampleNames)


@app.route("/otu")
def description():
    results = session.query(Otu.lowest_taxonomic_unit_found).all()

    otu_results = []

    for result in results:
        otu_results.append(result[0])

    return jsonify(otu_results)


@app.route("/metadata/<sample_id>")
def metaDataSample(sample_id):
    meta = getSampleMetaData(sample_id)
    return jsonify(meta)


@app.route("/wfreq/<sample_id>")
def washingFreq(sample_id):
    wfreq = getWashingFreq(sample_id)
    return jsonify(wfreq)


@app.route("/samples/<sample_id>")
def check(sample_id):
    return getOTUbySamples(sample_id)


if __name__ == "__main__":
    app.run()
