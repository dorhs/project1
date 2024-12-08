from flask import Blueprint, render_template, request, redirect, url_for
from app.vers import *


@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

