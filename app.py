from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import date


app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page showing all expenses
@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = c.fetchall()

    # Obtenir la somme totale des dépenses
    c.execute('SELECT SUM(amount) FROM expenses')
    total_amount = c.fetchone()[0] or 0.0

    conn.close()
    return render_template('index.html', expenses=expenses, total_amount=total_amount)

# Add new expense
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category']
        expense_date = request.form['date']

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('INSERT INTO expenses (name, amount, category, date) VALUES (?, ?, ?, ?)',
                  (name, amount, category, expense_date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_expense.html')

# Edit an expense
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category']
        expense_date = request.form['date']
        c.execute('UPDATE expenses SET name=?, amount=?, category=?, date=? WHERE id=?',
                  (name, amount, category, expense_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute('SELECT * FROM expenses WHERE id=?', (id,))
        expense = c.fetchone()
        conn.close()
        return render_template('edit_expense.html', expense=expense)

# Delete an expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Summary page
@app.route('/summary')
def summary():
    filter_category = request.args.get('filter_category')

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    if filter_category:
        c.execute('SELECT category, SUM(amount) FROM expenses WHERE category=? GROUP BY category', (filter_category,))
    else:
        c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    summary_data = c.fetchall()
    conn.close()

    labels = [row[0] for row in summary_data]
    values = [row[1] for row in summary_data]
    total_all = sum(values)

    # Génération de l'image du graphique avec matplotlib
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Pour un cercle parfait

    # Sauvegarder l'image dans une variable base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_img = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return render_template('summary.html', summary=summary_data, total_all=total_all, chart_img=chart_img)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

