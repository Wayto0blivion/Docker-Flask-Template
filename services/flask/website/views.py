"""
@author : Zuice
@date : 2024-10-19
"""

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from flask_login import login_required


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    """
    Simple landing page.
    :return: HTML Template: Home page.
    """
    # flash('Returned Home!', '')
    return render_template("home.html")


@views.route('/switch-theme/<theme>')
def switch_theme(theme):
    """
    Allows the user to switch between default Bootswatch Themes
    :param theme: String of theme to load.
    :return: Redirect to source or home
    """
    available_themes = ['cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 'litera', 'lumen', 'lux',
                        'materia', 'minty', 'pulse', 'sandstone', 'simplex', 'sketchy', 'slate', 'solar', 'spacelab',
                        'superhero', 'united', 'yeti', 'morph', 'quartz', 'vapor', 'zephyr']
    if theme in available_themes:
        session['theme'] = theme
    return redirect(request.referrer or url_for('views.home'))


@views.route('/site-map', methods=['GET'])
def site_map():
    """
    HTML page that contains a table with all links that don't require parameters.
    :return:
    """
    links = []
    for rule in current_app.url_map.iter_rules():
        # Exclude certain routes if necessary, like static files
        if 'GET' in rule.methods and len(rule.arguments) == 0:
            url = rule.rule
            endpoint = rule.endpoint
            links.append({'url': url, 'endpoint': endpoint})
            # Sort links
            links.sort(key=lambda x: x['url'])
    return render_template('sitemap.html', links=links)

