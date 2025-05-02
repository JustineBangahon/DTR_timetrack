import os
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

def parse_time(t):
    return datetime.strptime(t, '%I:%M %p') if t else None

@app.route('/', methods=['GET', 'POST'])
def index():
    rendered_hours = None
    if request.method == 'POST':
        day_type = request.form.get('day_type')
        if day_type == 'Whole Day':
            try:
                check_in = parse_time(request.form['check_in'])
                break_out = parse_time(request.form['break_out'])
                break_in = parse_time(request.form['break_in'])
                check_out = parse_time(request.form['check_out'])

                total_seconds = (break_out - check_in).total_seconds() + (check_out - break_in).total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                rendered_hours = f"{hours} Hours and {minutes:02d} Minutes"
            except Exception as e:
                rendered_hours = 'Invalid input. Please try again.'

        elif day_type == 'Half Day':
            try:
                check_in = parse_time(request.form['check_in_half'])
                check_out = parse_time(request.form['check_out_half'])

                total_seconds = (check_out - check_in).total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                rendered_hours = f"{hours} Hours and {minutes:02d} Minutes"
            except Exception as e:
                rendered_hours = 'Invalid input. Please try again.'

    return render_template('index.html', rendered_hours=rendered_hours)

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)