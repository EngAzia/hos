# web/templates/admin/web/emailsubscriber/change_list.html

{% extends "admin/change_list.html" %}
{% load static %}
{% block content %}

<h1>Custom message! habababababa</h1>

<!-- Render the rest of the ChangeList view by calling block.super -->
{{ block.super }}
{% endblock %}