import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration (Make sure MySQL is running)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://saurabh:%23S%40ushree@localhost/farm_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Database Models for Different Sections
class SeedSowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sowing_date = db.Column(db.String(20))
    seed_name = db.Column(db.String(100))
    seed_type = db.Column(db.String(50))
    seed_quantity = db.Column(db.Integer)
    land_preparation = db.Column(db.String(200))
    seed_cost = db.Column(db.Float)
    fertilizer_cost = db.Column(db.Float)

class Germination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    germination_days = db.Column(db.Integer)
    seedling_health = db.Column(db.String(200))
    fertilizer_type = db.Column(db.String(100))
    fertilizer_quantity = db.Column(db.Float)
    fertilizer_date = db.Column(db.String(20))
    fertilizer_price = db.Column(db.Float)

class VegetativeGrowth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    water_management = db.Column(db.String(100))
    fertilizer_usage = db.Column(db.String(200))
    pest_control = db.Column(db.String(200))
    weeding_done = db.Column(db.Boolean)
    pruning_done = db.Column(db.Boolean)
    pesticides_applied = db.Column(db.String(10))
    pesticide_type = db.Column(db.String(100))
    irrigation_type = db.Column(db.String(50))

class Harvesting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    harvesting_date = db.Column(db.String(20))
    yield_kg_per_acre = db.Column(db.Float)

class ExpensesProfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_cost = db.Column(db.Float)
    total_revenue = db.Column(db.Float)
    selling_location = db.Column(db.String(200))
    price_per_unit = db.Column(db.Float)
    profit_loss = db.Column(db.Float)

# ✅ Route to Display Dashboard with Saved Data
@app.route('/')
def index():
    seed_sowing_data = SeedSowing.query.all()
    germination_data = Germination.query.all()
    vegetative_data = VegetativeGrowth.query.all()
    harvesting_data = Harvesting.query.all()
    expenses_data = ExpensesProfit.query.all()

    return render_template('dashboard.html', 
                           seed_sowing_data=seed_sowing_data, 
                           germination_data=germination_data,
                           vegetative_data=vegetative_data,
                           harvesting_data=harvesting_data,
                           expenses_data=expenses_data)

# ✅ Routes to Save Data from Forms
@app.route('/save_seed_sowing', methods=['POST'])
def save_seed_sowing():
    data = SeedSowing(
        sowing_date=request.form.get('sowingDate'),
        seed_name=request.form.get('seedName'),
        seed_type=request.form.get('seedType'),
        seed_quantity=request.form.get('seedQuantity'),
        land_preparation=request.form.get('landPreparation'),
        seed_cost=request.form.get('seedCost'),
        fertilizer_cost=request.form.get('fertilizerCost')
    )
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/save_germination', methods=['POST'])
def save_germination():
    data = Germination(
        germination_days=request.form.get('germinationDays'),
        seedling_health=request.form.get('seedlingHealth'),
        fertilizer_type=request.form.get('fertilizerType'),
        fertilizer_quantity=request.form.get('fertilizerQuantity'),
        fertilizer_date=request.form.get('fertilizerDate'),
        fertilizer_price=request.form.get('fertilizerPrice')
    )
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/save_vegetative_growth', methods=['POST'])
def save_vegetative_growth():
    data = VegetativeGrowth(
        water_management=request.form.get('waterManagement'),
        fertilizer_usage=request.form.get('fertilizerUsage'),
        pest_control=request.form.get('pestControl'),
        weeding_done=bool(request.form.get('weedingDone')),
        pruning_done=bool(request.form.get('pruningDone')),
        pesticides_applied=request.form.get('pesticidesApplied'),
        pesticide_type=request.form.get('pesticideType'),
        irrigation_type=request.form.get('irrigationType')
    )
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/save_harvesting', methods=['POST'])
def save_harvesting():
    data = Harvesting(
        harvesting_date=request.form.get('harvestingDate'),
        yield_kg_per_acre=request.form.get('yield')
    )
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/save_expenses_profit', methods=['POST'])
def save_expenses_profit():
    def convert_to_float(value):
        """ Convert to float if not empty, else return None """
        return float(value) if value.strip() else None

    data = ExpensesProfit(
        total_cost=convert_to_float(request.form.get('totalCost', '0')),
        total_revenue=convert_to_float(request.form.get('totalRevenue', '0')),
        selling_location=request.form.get('sellingLocation'),
        price_per_unit=convert_to_float(request.form.get('pricePerUnit', '0')),
        profit_loss=convert_to_float(request.form.get('profitLoss', ''))
    )
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('index'))




@app.route('/delete/<string:table>/<int:id>', methods=['POST'])
def delete_entry(table, id):
    """ Delete an entry based on table name and ID """

    # Define the table mapping
    tables = {
        "seed_sowing": SeedSowing,
        "germination": Germination,
        "vegetative_growth": VegetativeGrowth,
        "harvesting": Harvesting,
        "expenses_profit": ExpensesProfit
    }

    # Check if table exists
    if table in tables:
        entry = db.session.get(tables[table], id)  # Fetch entry by ID
        if entry:
            db.session.delete(entry)
            db.session.commit()
            return redirect(url_for('index'))

    return "Entry not found", 404  # Return error if entry doesn't exist


# ✅ Run Flask App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
