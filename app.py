# Import the dependencies.
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite://?Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)
base.classes.keys()
# Save references to each table
Measurement = base.classes.measurement
Station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>" 
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of precipitation data for previous year"""
    # Query all precipitations and dates
    preYear = dt.datetime.strptime(lastDate,'%Y-%m-%d').date() - dt.timedelta(365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).\
                order_by(Measurement.date).all()
                    
    # Create a dictionary from the row data and append to a list of precipitations
    precipitations = {date: prcp for date, prcp in precipitation}
    session.close() 

    return jsonify(precipitations)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all stations"""
    # Query all stations
    session = Session(engine)

    """Return a list of all Stations"""
    # Query all Stations
    results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    """Return a list of temperatures and dates of previous year of most active station"""
    # Query most active station temperature and dates of previous year
    max_temp_obs = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.dt.datetime.strptime(lastDate,'%Y-%m-%d').date() - dt.timedelta(365)

    tobs_dict = dict(max_temp_obs)

    session.close()

    return jsonify(tobs_active)

@app.route("/api/v1.0/temp/<start>")
def start(start):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()

    for min,avg,max in result:
        start_tobs = {}
        start_tobs["Min"] = min
        start_tobs["Average"] = avg
        start_tobs["Max"] = max
        start_tobs.append(start_tobs_dict)
        
    return jsonify(start_tobs)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    tobs_all = []
    for min,avg,max in queryresult:
        start_end_tobs = {}
        start_end_tobs["Min"] = min
        start_end_tobs["Average"] = avg
        start_end_tobs["Max"] = max
        start_end_tobs.append(start_end_tobs_dict)

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)
    