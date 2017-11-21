---
layout: equipo
permalink: /malware/
---
<div class="row">
    <div class="col-sm-8">
        <div>
            {% for post in site.categories.article limit:site.recent_posts %}
            <div class="row amnesia_post-row">
                <h2 class="amnesia_post-title"><a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
                </h2>
                <span class="amnesia_post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
                <div class="amnesia_post-content">
                    {{ post.excerpt }}
                </div>
                <a href="{{ post.url | prepend: site.baseurl }}"><span
                        class="amnesia_post-readmore">Continue</span></a>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="col-sm-4">

        {% include archive_malware.html %}

    </div>
</div>
