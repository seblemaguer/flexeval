{% extends 'admin/base.tpl' %}

{% block content %}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> Admin Panel</h2>



  <div class="row">

    {% for tile in tiles%}

    <div class="col-6">

      <div class="card" style="margin-bottom:20px;">
        <div class="card-body">
          <h5 class="card-title">{{tile.title}}</h5>
          <p class="card-text">{{tile.description}}</p>
          <a href="{{tile.link}}" class="btn btn-primary">Access</a>
        </div>
      </div>
    </div>

    {% endfor %}


    </div>


{% endblock %}
