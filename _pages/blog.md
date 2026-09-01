---
layout: default
permalink: /blog/
title: blog
nav: true
nav_order: 3
pagination:
  enabled: true
  collection: posts
  permalink: /page/:num/
  per_page: 5
  sort_field: date
  sort_reverse: true
  trail:
    before: 1 # The number of links before the current page
    after: 3 # The number of links after the current page
_styles: >
  ul.post-list {
    padding-left: 0;
    list-style: none;
  }
  ul.post-list li.post-card {
    background: var(--global-card-bg-color);
    border: 1px solid var(--global-divider-color);
    border-radius: 12px;
    margin-bottom: 1.25rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }
  ul.post-list li.post-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
  }
  a.post-card-link {
    display: block;
    padding: 1.4rem 1.6rem;
    color: var(--global-text-color);
    text-decoration: none;
  }
  a.post-card-link:hover {
    color: var(--global-text-color);
    text-decoration: none;
  }
  h3.post-card-title {
    font-size: 1.45rem;
    font-weight: 700;
    margin: 0 0 0.5rem;
    color: var(--global-text-color);
  }
  p.post-card-excerpt {
    margin: 0 0 0.75rem;
    font-size: 0.98rem;
    opacity: 0.85;
  }
  p.post-card-meta {
    color: var(--global-text-color-light);
    font-size: 0.85rem;
    margin: 0;
  }
---

<div class="post">

{% assign blog_name_size = site.blog_name | size %}
{% assign blog_description_size = site.blog_description | size %}

{% if blog_name_size > 0 or blog_description_size > 0 %}

  <div class="header-bar">
    <h1>{{ site.blog_name }}</h1>
    <h2>{{ site.blog_description }}</h2>
  </div>
  {% endif %}

  <ul class="post-list">

    {% if page.pagination.enabled %}
      {% assign postlist = paginator.posts %}
    {% else %}
      {% assign postlist = site.posts %}
    {% endif %}

    {% for post in postlist %}

    {% if post.external_source == blank %}
      {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
    {% else %}
      {% assign read_time = post.feed_content | strip_html | number_of_words | divided_by: 180 | plus: 1 %}
    {% endif %}
    {% assign year = post.date | date: "%Y" %}
    {% assign tags = post.tags | join: "" %}
    {% assign categories = post.categories | join: "" %}

    <li class="post-card">
      {% if post.redirect == blank %}
        {% assign post_link = post.url | relative_url %}
      {% elsif post.redirect contains '://' %}
        {% assign post_link = post.redirect %}
      {% else %}
        {% assign post_link = post.redirect | relative_url %}
      {% endif %}
      <a class="post-card-link" href="{{ post_link }}" {% if post.redirect contains '://' %}target="_blank"{% endif %}>
        <h3 class="post-card-title">{{ post.title }}</h3>
        {% if post.description %}
          <p class="post-card-excerpt">{{ post.description }}</p>
        {% endif %}
        <p class="post-card-meta">
          Date: {{ post.date | date: '%B %-d, %Y' }}
          &nbsp;|&nbsp; Estimated Reading Time: {{ read_time }} min
          {% if post.author %}&nbsp;|&nbsp; Author: {{ post.author }}{% endif %}
          {% if post.external_source %}&nbsp;|&nbsp; {{ post.external_source }}{% endif %}
        </p>
      </a>
    </li>

    {% endfor %}

  </ul>

{% if page.pagination.enabled %}
{% include pagination.liquid %}
{% endif %}

</div>
