{% extends 'base.tpl' %}

{% block content %}

<h2 class="bd-content-title"> <img src="/assets/static/img/svg_icon/chevron-right.svg" alt=">" /> Test {{ name }} - step {{step}} over {{nb_step}}</h2>

<form action="./{{name}}/send" method="post"  enctype="multipart/form-data" class="form-example">

  <fieldset class="form-group">
    <legend class="col-form-label"><strong>Question:</strong> Between the following samples, which sample do you prefer in terms of <strong>quality</strong>?</legend>


    <div class="form-group">
    {% set name = save_field('choosen',systems()) %}
    {% for system in systems() %}

      <div class="form-check">
        <input class="form-check-input" type="radio" name="{{ name }}" id="sys{{ system.name() }}" value="{{ system.name() }}" checked>
        <label class="form-check-label" for="sys{{ system.name() }}">
          <img src="{{ obfuscate_assets(system.data[system.get_column_name(0)]) }}" />
        </label>
      </div>

    {% endfor %}
    </div>

  </fieldset>

  <button type="submit" class="btn btn-primary">Submit</button>

</form>
{% endblock %}
