import numpy as np
import pandas as pd
import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

# Flask Setup
app = Flask(__name__)

# Database Setup

from flask_sqlalchemy import SQLAlchemy

engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")

# Reflecting database into a new model
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)

# Save to class
Otu = Base.classes.otu
Metadata = Base.classes.samples_metadata
Samples = Base.classes.samples

session = Session(engine)


def __repr__(self):
    return '<Bio %r>' % (self.name)

# Create a route that return the dashboard homepage


@app.route("/")
def home():
    return render_template("index.html")

# Create a route that renders a list of the sample names


@app.route("/names")
def names_list():
    # Create inspecor and connect it to the engine
    inspector = inspect(engine)

    # Collect the names of the tables within the database
    tables = inspector.get_table_names()

    # Using the inspector to print the column names of tables
    columns = inspector.get_columns("samples")

    names = []

    for column in columns[1:]:
        names.append(column["name"])

    return jsonify(names)

# List of OTU descriptions


@app.route("/otu")
def description():
    results = session.query(Otu.lowest_taxonomic_unit_found).all()

    otu_results = []

    for result in results:
        otu_results.append(result[0])

    return jsonify(otu_results)

# MetaData for a given sample


@app.route("/metadata/<sample>")
def sample_meta(sample):
    sample_id = sample[3:]

    result = session.query(Metadata.AGE, Metadata.BBTYPE, Metadata.ETHNICITY, Metadata.GENDER, Metadata.LOCATION, Metadata.SAMPLEID).filter(Metadata, SAMPLEID == sample_id).first()

    metadict = {
        "AGE": result[0],
        "BBTYPE": result[1],
        "ETHNICITY": result[2],
        "GENDER": result[3],
        "LOCATION": result[4],
        "SAMPLEID": result[5]
    }

    return jsonify(metadict)
