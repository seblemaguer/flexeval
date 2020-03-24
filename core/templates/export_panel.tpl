{% extends 'base.tpl' %}

{% block title %} Export {% endblock %}


{% block content %}
  <h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Export</h2>

  <div class="row">
    <div class="col-sm-6">

      <div class="card">
        <div class="card-body">
          <h5 class="card-title">CSV</h5>
          <p class="card-text">Download a zip repository containing the database dumped in csv files and <a href="https://developer.mozilla.org/fr/docs/Web/API/Blob">blob files.</a></p>
          <a href="bdd.zip?password={{password}}" class="btn btn-primary">Download</a>
        </div>
      </div>

    </div>
    <div class="col-sm-6">

      <div class="card">
        <div class="card-body">
          <h5 class="card-title">SQLite</h5>
          <p class="card-text">Download the sqlite base.</p>
          <a href="bdd.sqlite?password={{password}}" class="btn btn-primary">Download</a>
        </div>
      </div>

    </div>
  </div>

  <a href="/"> Back </a>

{% endblock %}
