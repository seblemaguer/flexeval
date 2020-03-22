{% extends 'core/base.tpl' %}

{% block title %}ERREUR {{code}}{% endblock %}

{% block content %}

  <h2> Erreur {{code}} </h2>

  <p> Une erreur s'est produite </p>

  <a href="{{entrypoint}}"> Retour à l'accueil </a>

{% endblock %}

{% block footer %}
{% endblock %}
