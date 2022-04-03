<template>
    <div style="padding: 50px">
        <el-form :model="form" label-width="150px">
            <el-form-item label="Name">
                <el-col :span="10">
                    <el-input v-model="form.name" />
                </el-col>
            </el-form-item>
            <el-form-item label="Description">
                <el-input v-model="form.description" type="textarea" :rows="3"/>
            </el-form-item>
            <el-form-item label="Deadline">
                <el-date-picker
                    v-model="deadline"
                    type="datetime"
                    placeholder="Select date and time"
                    value-format="YYYY-MM-DDThh:mm:ss Z"
                />
            </el-form-item>
            <el-form-item label="Upload limit">
                <el-col :span="10">
                    <el-input v-model="form.upload_limit" />
                </el-col>
            </el-form-item>
            <el-tooltip class="box-item"
                        effect="dark"
                        content="in seconds"
                        placement="top-start">
                <el-form-item label="Running time limit">
                    <el-col :span="10">
                        <el-input v-model="form.running_time_limit" />
                    </el-col>
                </el-form-item>
            </el-tooltip>
            <el-form-item label="Concurrent limit">
                <el-col :span="10">
                    <el-input v-model="form.concurrent_limit" disabled placeholder="1" />
                </el-col>
            </el-form-item>
            <el-form-item label="Ordering">
                <el-radio v-model="descendent" :label="true" size="large">Descendent</el-radio>
                <el-radio v-model="descendent" :label="false" size="large">Ascendant</el-radio>
            </el-form-item>
            <el-tooltip class="box-item"
                        effect="dark"
                        content="referenced query to get the expected result"
                        placement="top-start">
                <el-form-item label="Reference Query">
                    <input  type="file" @change="getFile('reference_query')" id="reference_query" accept=".sql"/>
                </el-form-item>
            </el-tooltip>
            <el-tooltip class="box-item"
                        effect="dark"
                        content=".txt file with all the competitors' emails, separated with semicolon"
                        placement="top-start">
                <el-form-item label="Competitors">
                    <input  type="file" @change="getFile('competitor_info')" id="competitor_info" accept=".txt"/>
                </el-form-item>
            </el-tooltip>
            <el-tooltip class="box-item"
                        effect="dark"
                        content=".sql file to insert data into public database"
                        placement="top-start">
                <el-form-item label="Public dataset">
                    <input  type="file" @change="getFile('public_sql')" id="public_sql" accept=".sql"/>
                </el-form-item>
            </el-tooltip>
            <el-tooltip class="box-item"
                        effect="dark"
                        content=".sql file to insert data into private database"
                        placement="top-start">
                <el-form-item label="Private dataset">
                    <input  type="file" @change="getFile('private_sql')" id="private_sql" accept=".sql"/>
                </el-form-item>
            </el-tooltip>
        </el-form>
        <el-row>
            <el-button type="primary" @click="onSubmit">Create</el-button>
            <el-button>Cancel</el-button>
        </el-row>
    </div>
</template>

<script lang="ts" setup>
import {reactive, ref} from 'vue'
import type { UploadUserFile, UploadProps,UploadInstance } from 'element-plus/lib/el-upload/src'
import {ElMessage, ElMessageBox} from "element-plus";
import {postCompetitionApi} from "@/api/competition";
import store from "@/store";
const deadline = ref('')
// do not use same name with ref
const descendent = ref(true)

const form = reactive({
    name: '',
    description: '',
    upload_limit:'',
    concurrent_limit: 1,
    running_time_limit:'',
})

const formData = new FormData()

const getFile = (target) => {
    switch (target) {
        case "reference_query":
            data.append("reference_query", document.getElementById("reference_query").files[0])
            break
        case "competitor_info":
            data.append("competitor_info", document.getElementById("competitor_info").files[0])
            break
        case "public_sql":
            data.append("public_sql", document.getElementById("public_sql").files[0])
            break
        case "private_sql":
            data.append("private_sql", document.getElementById("private_sql").files[0])
            break
        default:
            break
    }
}

const onSubmit = () => {
    console.log('submit!')
    console.log(deadline.value)

    data.append("name", form.name)
    data.append("description", form.description)
    data.append("upload_limit", form.upload_limit)
    data.append("concurrent_limit", form.concurrent_limit.toString())
    data.append("running_time_limit", form.running_time_limit)
    data.append("end_time", deadline.value)
    if (descendent.value) {
        data.append("descendent_ordering", "true")
    } else {
        data.append("descendent_ordering", "false")
    }
    postCompetitionApi(data).then((res) => {})
    /*postCompetitionApi(form.name, form.description, form.upload_limit, form.concurrent_limit,
        form.running_time_limit, deadline.value, descendent.value, files).then(() => {})*/
}

const data = new FormData()

const uploadHttpRequest = (data) => {
    let reader = new FileReader()
    let that = this
    reader.readAsText(data.file)

    /*reader.onload = function() {
        that.formData.mmiapXml = this.result
    }*/
}
</script>

<style lang="scss" scoped>
.tooltip-base-box .box-item {
    width: 110px;
    margin-top: 10px;
}
.contact-box{
    width: 70vw;
    margin: 0 auto;
    padding: 50px;
    .git{
        padding: 10px 20px;
        border-radius: 5px;
        width: fit-content;
        margin-bottom: 20px;
        font-weight: 600;
        a{
            color: rgb(250, 45, 45);
        }
    }
    .info{
        display: flex;
        align-items: center;
        justify-content: space-around;
        text-align: center;
        margin-top: 20px;
        img{
            width: 300px;
            height: 300px;
        }
        div{
            font-size: 20px;
            font-weight: 600;
        }
    }
    .hint{
        text-align: center;
        color: rgb(247, 77, 77);
        margin-top: 50px;
    }
}
</style>