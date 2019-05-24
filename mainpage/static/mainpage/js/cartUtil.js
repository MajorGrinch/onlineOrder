Vue.config.devtools = true;

var eventBus = new Vue();

Vue.component('restaurant-card', {
    props: {
        cart: {
            type: Object,
            required: true
        },
    },
    template: `
    <div id="my_cart_div">
        <div v-show="Object.keys(cart).length === 0" class="text-center">
            <h1>Cart is empty</h1>
        </div>
        <div v-for="restaurant in cart">
            <div class="card restaurant-card">
                <div class="card-header">
                    <b><a v-bind:href="restaurant_url(restaurant.id)">{{restaurant.name}}</a></b>
                </div>
                <div class="card-body">
                    <div v-for="menu_item_info in restaurant.iteminfo_list" class="card mb-3" style="max-width: 100%;">
                        <div class="row no-gutters">
                            <div class="col-md-3">
                                <img style="height:12rem;" v-bind:src="getImgUrl(menu_item_info.image)" class="card-img" alt="...">
                            </div>
                            <div class="col-md-9">
                                <div class="card-body">
                                    <h5 class="card-title">{{menu_item_info.title}}</h5>
                                    <p class="card-text">Area kept for use</p>
                                    <div class="row">
                                        <div class="col">
                                            <label>Quantity: &nbsp</label>

                                            <input type="number" v-model.number="menu_item_info.quantity" class="form-control" style="width:auto;">
                                        </div>
                                        <div class="col text-right">
                                                <label>Unit Price: &nbsp</label><b class="item_price">\${{menu_item_info.price}}</b>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-footer">
                    <div class="row">
                        <div class="col text-left">
                            <span class="subtotal_span">Subtotal:</span>
                            <b class="subtotal_price" value="10">\${{subtotal(restaurant)}}</b>
                        </div>
                        <div class="col text-right">
                            <button type="button" class="btn btn-primary">
                                Place Order
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            </br>
        </div>
    </div>`,
    data(){
        return {
            MEDIA_URL: 'http://127.0.0.1:8000/media/',
            root_url: 'http://127.0.0.1:8000/'
        }
    },
    computed:{
    },
    methods:{
        restaurant_url(restaurant_id){
            return this.root_url + 'restaurant_menu/' + parseInt(restaurant_id.substring(11));
        },
        getImgUrl(image_path){
            return this.MEDIA_URL + image_path;
        },
        subtotal(restaurant){
            var subtotal = 0;
            var iteminfo_list = restaurant.iteminfo_list;
            // console.log(iteminfo_list);
            for (var key in iteminfo_list) {
                // console.log(iteminfo_list[key]);
                iteminfo = iteminfo_list[key];
                subtotal += iteminfo['price'] * iteminfo['quantity'];
            }
            this.$emit('update-cart');
            this.saveCart2Cookie();
            return subtotal;
        },
        getItemQuantity(){
            return 1;
        },
        saveCart2Cookie(){
            // console.log(this.cart);
            Cookies.set('cart', this.cart);
        }
    }
})


var cart_app = new Vue({
    el: '#cart_app_div',
    data: {
        cart: getCart()
    },
    methods:{
        showCart(){
            console.log(this.cart)
        }
    }
})