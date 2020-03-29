{% extends 'admin/base.tpl' %}

{% block content %}
  <h2 class="bd-content-title"> <img src="{{make_url('/assets/static/img/svg_icon/chevron-right.svg')}}" alt=">" /> Member</h2>

  <p> Without invitation people can't join this website.</p>

  <div class="row">

    <div class="col-6">

      <div class="card" style="margin-bottom:20px;">
        <div class="card-body">
          <h5 class="card-title">Invitation</h5>
          <p class="card-text">Send an invitation by email.</p>
          <a href="./invite" class="btn btn-primary">Access</a>
        </div>
      </div>
    </div>

    <div class="col-6">

      <div class="card" style="margin-bottom:20px;">
        <div class="card-body">
          <h5 class="card-title">Configuration</h5>
          <p class="card-text">To be able to send invitations you need to configure our mail box.</p>
          <a href="./email-param" class="btn btn-primary">Configure</a>
        </div>
      </div>
    </div>

    <div class="col-6">

      <div class="card" style="margin-bottom:20px;">
        <div class="card-body">
          <h5 class="card-title">Pending Invitation</h5>
          <p class="card-text"> List of all the invitation send.</p>
          <a href="./pending-invitation" class="btn btn-primary">Access</a>
        </div>
      </div>
    </div>

  </div>

  <a href="{{make_url('/admin') }}"> Back to admin panel.</a>

{% endblock %}
