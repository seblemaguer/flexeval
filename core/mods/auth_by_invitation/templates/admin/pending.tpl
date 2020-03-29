{% extends 'admin/base.tpl' %}



{% block content %}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> Pending Invitation</h2>
  <p> When sending an invitation is considered as pending, until the receiver click on the invitation link.</p>
  <table class="table table-hover">
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Email</th>
        <th scope="col">Pending?</th>
      </tr>
    </thead>
    <tbody>
      {% for w in users%}
      <tr>
        <th scope="row">{{w.id}}</th>
        <td>{{w.email}}</td>
        <td>{% if w.activated %}No{% else %}Yes{% endif %}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <p><a href="./"> Back</a></p>

{% endblock %}
