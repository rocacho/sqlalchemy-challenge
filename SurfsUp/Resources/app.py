# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
class_names = list(Base.classes.keys())
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# Create the app
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# Start at the homepage.
# List all the available routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route('/api/v1.0/precipitation')
def precipitation():
    """Last 12 months of precipitation"""
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = (
        session
        .query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= one_year_ago)
        .all()
    )
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

# Return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    """Stations"""
    results = session.query(Measurement.station).distinct().all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.

@app.route('/api/v1.0/tobs')
def tobs():
    """Dates and temperature observations of the most-active station"""
    one_year_ago_sation = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    results = (
        session
        .query(Measurement.date, Measurement.tobs)
        .filter(Measurement.station == 'USC00519281')
        .filter(Measurement.date >= one_year_ago_sation)
        .all()
    )
    temperature_data = {date: tobs for date, tobs in results}
    return jsonify(temperature_data)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# app route temp stats start
@app.route('/api/v1.0/<start>')
def temp_stats_start(start):
    """Temperature statistics for Start Date: 2016-08-18"""
    results = (
        session
        .query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)
        )
        .filter(Measurement.station == 'USC00519281')
        .filter(Measurement.date >= '2016-08-18')
        .all()
    )
    temp_stats = {
        'TMIN': results[0][0],
        'TMAX': results[0][1],
        'TAVG': results[0][2]
    }
    return jsonify(temp_stats)

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
# app route temp stats start & end

@app.route('/api/v1.0/<start>/<end>')
def temp_stats_start_end(start, end):
    """Temperature statistics for a specified start and end date: 2016-08-18 & 2017-08-18."""
    results = (
        session
        .query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)
        )
        .filter(Measurement.station == 'USC00519281')
        .filter(Measurement.date >= '2016-08-18')
        .filter(Measurement.date <= '2017-08-18')
        .all()
    )
    temp_stats = {
        'TMIN': results[0][0],
        'TMAX': results[0][1],
        'TAVG': results[0][2]
    }
    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)