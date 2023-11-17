from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import numpy as np

#################################################
# Database Setup
#################################################
db_path = "Resources/hawaii.sqlite"
    
# Database Setup with specified file path
engine = create_engine(f"sqlite:///{db_path}")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the date and precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()

    session.close()

    # Convert the query results to a dictionary with date as key and prcp as value
    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all statios"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Add filters for the most active station and data for the last year
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.station == 'USC00519281', Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()
        
    session.close()

    # Process 'results' and return the data
    temperatures_list = []
    for date, temperature in results:
        temp_dict = {"date": date, "temperature": temperature}
        temperatures_list.append(temp_dict)

    return jsonify(temperatures_list)

if __name__ == '__main__':
    app.run(debug=True)