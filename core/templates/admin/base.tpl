{% extends 'base.tpl' %}

{%block bottomlink%}
  <p class="text-muted" style="letter-spacing: 2px;">
    <a href="{{make_url('/')}}"> Back to test</a>.
  </p>
{%endblock%}

{%block userintel%}
  <a href="{{make_url('/admin/deco')}}"> Log out </a>
{%endblock%}
