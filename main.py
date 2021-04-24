from app import app, db
from app.models import User, Problem
from app.math_text_converter import MathTextConverter

if __name__ == '__main__':
    app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Problem': Problem}
