from flask import Blueprint, render_template, request
from lvl0_character import Character

lvl0_bp = Blueprint('lvl0', __name__)


@lvl0_bp.route('/lvl0')
def level0():
    # Add your character generator logic here
    # For now, let's render a template
    return render_template('lvl0_creation_form.html', title='Level 0 Character Generator')

@lvl0_bp.route('/lvl0/generate_character', methods=['GET', 'POST'])
def generate_character():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        character_name = request.form.get('character_name')
        random_name = request.form.get('random_name')
        gender = request.form.get('gender')
        race = request.form.get('race')

        character = Character(player_name=player_name, random_name=random_name, character_name=character_name, gender=gender, race=race)
        # ... generate character attributes, stats, and inventory

        character_sheet_content = render_template('lvl0_character_sheet.html', character=character)

        # Save character sheet as an HTML file
        #save_character_sheet(character.character_name, character_sheet_content)

        return render_template('lvl0_character_sheet.html', character=character)

def save_character_sheet(character_name, content):
    file_path = f'character_sheets/{character_name}_sheet.html'  # Adjust path as needed
    with open(file_path, 'w') as file:
        file.write(content)
