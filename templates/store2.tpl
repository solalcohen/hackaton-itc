<h1>Our Products</h1>
<div class="browse">
<div class="show" id="myPopup">
<span >Buy this item and join 2 of your community members, Solal and Shai, to benefit from this weeks 3 for 2 special!</span>
</div>
% for article in result:
    <article class="clickable shadowed" onmouseover="myFunction()" onmouseout="myFunction2()"  id='{{article['id_product']}} '>
    <div class="price">
          <i class="fas fa-star"></i><span class="average">{{article['price']}}</span>
    </div>
    <div class="logo">
          <i class="fas fa-star"></i><span class="average"><img src={{article['supermarket_image']}}></img></span>
    </div>
     <div class="cover-holder">
                <img src="{{article['product_image']}}" class="show-cover"/>
        </div>

        <h3 class="show-name">{{article['product_name']}}</h3>
    </article>
% end
</div>
</div>