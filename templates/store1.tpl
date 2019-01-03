    <h1>Hello admin from community n°3 ! </h1>
    <h3>Choose your categorie</h3>
    <div class="browse">
        % for article in result:
            <article class="clickable shadowed" onclick="Browse.loadShow('{{article['id']}}')">
                <div class="cover-holder">
                    <img src="{{article['category_image']}}" class="show-cover"/>
                </div>
                <h3 class="show-name">{{article['category']}}</h3>
            </article>
        % end
    </div>
