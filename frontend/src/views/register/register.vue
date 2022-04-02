<template>
    <div class="clearfix" id="login_wrap">
        <h2 class="title">Register</h2>
        <div id="login">
            <div class="login--account">
                <span>Email: </span>
                <el-input type="text"
                          name="email"
                          v-model="email">

                </el-input>
            </div>
            <div class="login--account">
                <span>Username: </span>
                <el-input type="text"
                          name="username"
                          v-model="username">

                </el-input>
            </div>
            <div class="login--password">
                <span>Password: </span>
                <el-input type="password"
                          name="password"
                          v-model="password">

                </el-input>
            </div>
            <p class="login--btn">
                <button class="theme-all" id="loginBtn" @click="registerFunc">Register</button>
            </p>
            <el-row :gutter="10" type="flex">
                <el-col :span="100">
                    <span>Already Have One?
                        <router-link :to="{ path: '/login'}">
                            <el-link type="primary">Log In</el-link>
                        </router-link>
                    </span>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import {registerApi} from "@/api/register";
import {ElNotification} from "element-plus";
export default defineComponent({
    setup() {
    },
    data() {
        return {
            email: "",
            username: "",
            password: ""
        }
    },
    methods: {
        registerFunc() {
            let check = this.checkParameter()
            if (check != null) {
                ElNotification({
                    title: 'Error',
                    message: 'Please enter correct ' + check,
                    type: 'error',
                    duration: 1500
                })
                return
            }
            //registerApi(this.email, this.username, this.password).then(()=>{})
            this.$router.push({path: "/login"})
        },
        checkParameter() {
            let reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
            if (this.email == "" || !reg.test(this.email)) {
                return "email"
            }
            if (this.username == "") {
                return "username"
            }
            if (this.password == "") {
                return "password"
            }
            return
        }
    }
})
</script>

<style scoped lang="scss">
.title {
    text-align: center;
    font-size: 22px;
    padding-top: 100px;
}
.el-link_item {
    display: inline-block;
    width: 400px;
    font-size: 20px;
}
#login_wrap {
    position: relative;
    background: rgba(64, 64, 194, 0.1);
    height: 100vh;
    > div {
        background: #fff;
        width: 479px;
        height: 495px;
        padding: 30px 40px;
        position: absolute;
        top: 48%;
        left: 50%;
        transform: translate(-50%, -50%);
        > div {
            padding: 10px 0;
            border-bottom: 1px solid #ddd;
            &.login--account {
                margin: 25px 0 30px;
            }
            span {
                color: #666;
                display: inline-block;
                width: 400px;
                font-size: 20px;
            }
            input {
                background: none;
                font-size: 16px;
                border: none;
                height: 30px;
                width: 200px;
                padding-left: 12px;
                box-sizing: border-box;
                color: #666;
                &.error {
                    border: 1px solid #f00;
                }
                &::-webkit-input-placeholder {
                    color: #aaa;
                }
            }
        }

        p {
            text-align: right;
            &.login--btn {
                button {
                    width: 100%;
                    height: 50px;
                    font-size: 18px;
                    background: #0f6171;
                    border: none;
                    margin-top: 30px;
                    color: #fff;
                    border-radius: 6px;
                    cursor: pointer;
                }
            }
            a {
                color: #fff;
                display: inline-block;
                padding: 0 15px;
                font-size: 14px;
            }
        }
    }
}
</style>
