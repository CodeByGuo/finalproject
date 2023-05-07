from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

admins = {
    'admin1': '12345',
    'admin2': '24680',
    'admin3': '98765'
}

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def read_reservations():
    reservations = []
    if Path('data/reservations.txt').is_file():
        with open('data/reservations.txt', 'r') as file:
            for line in file.readlines():
                reservations.append(line.strip().split(','))
    return reservations

def save_reservation(reservation):
    with open('data/reservations.txt', 'a') as file:
        file.write(','.join(reservation) + '\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']
        if admin_username in admins and admins[admin_username] == admin_password:
            return redirect(url_for('admin', admin_username=admin_username))
        else:
            flash("Invalid username or password. Please try again.")
    return render_template('login.html')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        row = request.form['row']
        column = request.form['column']
        e_ticket = f"{random.randint(100000, 999999)}"
        reservation = [first_name, last_name, row, column, e_ticket]
        save_reservation(reservation)
        return redirect(url_for('reservation_success', first_name=first_name, last_name=last_name, row=row, column=column, e_ticket=e_ticket))
    reservations = read_reservations()
    seating_chart = [[None for _ in range(4)] for _ in range(12)]
    for r in reservations:
        seating_chart[int(r[2])][int(r[3])] = f"{r[0]} {r[1]}"
    cost_matrix = get_cost_matrix()
    return render_template('reservation.html', cost_matrix=cost_matrix, seating_chart=seating_chart)

@app.route('/reservation_success', methods=['GET'])
def reservation_success():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    row = request.args.get('row')
    column = request.args.get('column')
    e_ticket = request.args.get('e_ticket')
    return render_template('reservation_success.html', first_name=first_name, last_name=last_name, row=row, column=column, e_ticket=e_ticket)

@app.route('/admin', methods=['GET'])
def admin():
    admin_username = request.args.get('admin_username')
    reservations = read_reservations()
    cost_matrix = get_cost_matrix()
    total_sales = sum(cost_matrix[int(r[2])][int(r[3])] for r in reservations)
    seating_chart = [[None for _ in range(4)] for _ in range(12)]
    for r in reservations:
        seating_chart[int(r[2])][int(r[3])] = f"{r[0]} {r[1]}"
    return render_template('admin.html', admin_username=admin_username,seating_chart=seating_chart, total_sales=total_sales, cost_matrix=cost_matrix)

if __name__ == '__main__':
    app.run(debug=True)

