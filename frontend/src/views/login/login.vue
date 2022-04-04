<template>
    <div class="clearfix" id="login_wrap">
        <h2 class="title">Sign In</h2>
        <div id="login">
            <div class="login--account">
                <span>Email: </span>
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
                <button class="theme-all" id="loginBtn" @click="loginFunc">Sign In</button>
            </p>
            <el-row :gutter="10" type="flex">
                <el-col :span="100">
                    <span>Haven't registered?
                        <router-link :to="{ path: '/register'}">
                            <el-link type="primary">Go register</el-link>
                        </router-link>
                    </span>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue'
import {loginApi} from "@/api/login";
import { useRouter } from 'vue-router';
import {useStore} from "vuex";
import {ElNotification} from "element-plus";
export default defineComponent({
    data() {
        return {
            username: "",
            password: ""
        }
    },
    methods: {
        loginFunc() {
            loginApi(this.username, this.password).then((res:any) => {
                console.log("res: " + res)
                if (res.token != null) {
                    this.$router.push({path: "/leaderboard"})
                } else {
                    ElNotification({
                        title: 'Error',
                        message: 'Please register',
                        type: 'error',
                        duration: 1500
                    })
                }
            })
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
        height: 370px;
        padding: 30px 40px;
        position: absolute;
        top: 40%;
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
