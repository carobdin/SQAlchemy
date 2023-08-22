# Import the dependencies.
from flask import Flask



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
   
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    precipitation_dict = one_year.set_index('date')['prcp'].to_dict()
    
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    
    results = session.query(Station.station).all()
    
    session.close()
    
    all_stations= list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def stations():
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    most_active_station = session.query(Measurement.date, Measurement.tobs).\
filter (Measurement.station == 'USC00519281', Measurement.date <= '2017-08-23', Measurement.date >= query_date).all()

    session.close()
    # Return a JSON list of temperature observations for the previous year.

    return jsonify(most_active_station)

if __name__ == '__main__':
    app.run()

