Vue.component('restaurant-order', {
    props:{
        order_id:{
            type: Number,
            required: true
        },
    },
    template:`
    <div>
        <div v-for="order_item in order_item_list" class="card mb-3" style="max-width: 100%;">
            <div class="row no-gutters">
                <div class="col-md-3">
                    <img style="height:12rem;" v-bind:src="base_url + 'media/'+order_item.image" class="card-img" alt="#">
                </div>
                <div class="col-md-9">
                    <div class="card-body">
                        <h5 class="card-title"><a :href="base_url + 'restaurant_menu/' + order_item.restaurant_id">{{order_item.title}}</a></h5>
                        <p class="card-text">Unit price \${{order_item.unit_price}}</p>
                        <p class="card-text">Quantity &times; <b>{{order_item.quantity}}</b></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    data(){
        return{
            order_item_list: null,
            base_url: 'http://127.0.0.1:8000/'
        }
    },
    method: {
        test(){
            console.log('test')
        }
    },
    mounted: function() {
        this.$http.get(this.base_url + 'get_order_detail/' + this.order_id)
        .then(response=>{
            // console.log(response);
            this.order_item_list = response.body;
        }, response =>{
            // console.log(response)
        })
    }
})
var orderlist_app = new Vue({
    el: '#orderlist_app_div',
    data: {
    },
    method: {

    }
})