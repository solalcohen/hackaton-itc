<h1>Our Products</h1>
<div class="browse">
% for article in result:
    <article class="clickable shadowed" onclick="Browse.loadEpisode('{{article['id']}}')">
        <div class="cover-holder">
                <img src="{{article['product_image']}}" class="show-cover"/>
        </div>
        <h3 class="show-name">{{article['product_name']}}</h3>
    </article>
% end
</div>
</div>