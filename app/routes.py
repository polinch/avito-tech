from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Ad


@app.route('/ads', methods=['GET'])
def get_all_ads():
    pass


@app.route('/ads/<id>', methods=['GET'])
def get_ad(id):
    pass


@app.route('/ads/<id>?fields', methods=['GET'])
def get_ad_fields(id):
    pass


@app.route('/new', methods=['GET', 'POST'])
def create_ad():
    pass
