import VueRouter from "vue-router"
import Main from "@/components/Main.vue";
import Vue from "vue";
import Login from "@/components/Login.vue";

Vue.use(VueRouter)
const router = new VueRouter({
    routes:[
        {
            path:"/login",
            name:"login",
            component:Login,
            meta:{
                keepalive:false
            }
        },
        {
            path: "/",
            name:"main",
            component: Main,
            meta:{
                keepalive: true
            }
        },
        {
            path:"/graph",
            name:"graph",
            component:()=>import("@/components/KnowledgeGraph.vue"),
            meta:{
                keepalive: true
            }

        },
        {
            path:"/water_flow",
            name:"water_flow",
            component: ()=>import("@/components/WaterFlow.vue"),
            meta:{
                keepalive:true
            }
        }
    ]
})

router.beforeEach((to,from,next)=>{
    if(to.meta.keepalive){
        if(localStorage.getItem("login")==="login"){
            next()
        }else{
            router.push("/login")
        }
    }else{
        next()
    }
})

export default router