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
                            <span>(\${{getDeliverFee(restaurant)}} deliver fee)</span>
                        </div>
                        <div class="col text-right">
                            <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#choose_address_modal" id="toggle_choose_address_modal_btn" @click="getAddressList(restaurant.id)">
                                Place Order
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            </br>
        </div>
        <div class="modal fade" id="choose_address_modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalCenterTitle">Modal title</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        Place address at here
                        <div v-for="(address,index) in address_list" class="custom-control custom-radio">
                            <input v-if="address.fields.is_default" type="radio" :id="'customRadio'+index" name="customRadio" class="custom-control-input" checked>
                            <input v-else type="radio" :id="'customRadio'+index" name="customRadio" class="custom-control-input">
                            <label class="custom-control-label" :for="'customRadio'+index" @click="useAddress(address)">
                                <span v-for="field in address.fields">
                                    {{field}}
                                </span>
                            </label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="placeOrder">Place Order</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`,
    data(){
        return {
            root_url: window.location.origin,
            MEDIA_URL: window.location.origin + '/media/',
            address_list:[],
            selected_restaurant : null,
            selected_address : null,
        }
    },
    computed:{
    },
    methods:{
        restaurant_url(restaurant_id){
            return this.root_url + '/restaurant_menu/' + parseInt(restaurant_id.substring(11));
        },
        getImgUrl(image_path){
            return this.MEDIA_URL + image_path;
        },
        subtotal(restaurant){
            var subtotal = restaurant.delivering_fee;
            var iteminfo_list = restaurant.iteminfo_list;
            // console.log(iteminfo_list);
            for (var key in iteminfo_list) {
                // console.log(iteminfo_list[key]);
                iteminfo = iteminfo_list[key];
                subtotal += iteminfo['price'] * iteminfo['quantity'];
            }
            // this.$emit('update-cart');
            restaurant['subtotal'] = subtotal;
            this.saveCart2Cookie();
            return subtotal;
        },
        getItemQuantity(){
            return 1;
        },
        saveCart2Cookie(){
            // console.log(this.cart);
            var username = Cookies.get('current_user');
            Cookies.set(username+'-cart', this.cart);
        },
        getDeliverFee(restaurant){
            // console.log(restaurant.delivering_fee);
            return restaurant.delivering_fee;
        },
        placeOrder(){
            // console.log(restaurant);
            this.$http.post(this.root_url + '/place_order/',
            {
                restaurant_cart: this.cart[this.selected_restaurant],
                address_id: this.selected_address
            },
            {
                headers: {'X-CSRFToken': Cookies.get('csrftoken')}
            }).then(response => {
                if(response.bodyText == 'No address choosed'){
                    // alert("You haven't set a address");
                }
                else{
                    var restaurant_id = response.bodyText;
                    console.log('delete ' + restaurant_id);
                    Vue.delete(this.cart, restaurant_id);
                    this.saveCart2Cookie();
                }
                location.reload();
            }, response => {
                console.log(response);
            })
        },
        getAddressList(restaurant_id){
            this.$http.post(this.root_url + '/cart_detail/', {}, {
                headers: {'X-CSRFToken': Cookies.get('csrftoken')}
            }).then(response => {
                console.log(response.body);
                var data = response.body;
                this.address_list = []
                for(index in data){
                    this.address_list.push(data[index])
                }
            })
            this.selected_restaurant = restaurant_id;
        },
        useAddress(address){
            console.log(address);
            this.selected_address = address.pk;
        }
    }
})


var cart_app = new Vue({
    el: '#cart_app_div',
    data: {
        cart: getCart(),
        base_url : Cookies.get('base_url')
    },
    methods:{
        showCart(){
            console.log(this.cart)
        }
    }
})