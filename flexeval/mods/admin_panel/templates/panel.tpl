{% extends get_template('base.tpl') %}

{% block content %}

  <h2 class="bd-content-title"> <img src="{{get_asset('/img/svg_icon/chevron-right.svg','flexeval')}}" alt=">" /> {{get_variable("subtitle",default_value="Admin Panel")}}</h2>

  <div class="row">

    {% for admin_module in get_variable("admin_modules")%}

    <div class="col-6">

      <div class="card" style="margin-bottom:20px;">
        <div class="card-body">
          <h5 class="card-title">{{admin_module.title}}</h5>
          <p class="card-text">{{admin_module.description}}</p>
          <a href="{{admin_module.url}}" class="btn btn-primary">Access</a>
        </div>
      </div>
    </div>

    {% endfor %}


    </div>


{% endblock %}
