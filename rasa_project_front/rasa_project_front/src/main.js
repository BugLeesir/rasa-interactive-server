import Vue from 'vue'
import App from './App.vue'
import store from "./store/index"
import router from "@/pages/index"
import {Container,Header,Aside,Main,Button,Row,Col,Menu,Submenu,Card,Form,FormItem,Input} from "element-ui"

Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Button)
Vue.use(Row)
Vue.use(Col)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(Card)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  store,router
}).$mount('#app')
