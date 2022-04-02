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
            <el-form-item label="Competition">
                <el-date-picker
                    v-model="deadline"
                    type="datetime"
                    placeholder="Select date and time"
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
                    <el-upload
                        class="upload-demo"
                        action="https://jsonplaceholder.typicode.com/posts/"
                        :limit="1"
                        :on-change="handleUploadChange"
                    >
                        <el-button type="primary">Click to upload</el-button>
                    </el-upload>
                </el-form-item>
            </el-tooltip>
            <el-tooltip class="box-item"
                        effect="dark"
                        content=".txt file with all the competitors' emails, separated with semicolon"
                        placement="top-start">
                <el-form-item label="Competitors">
                    <el-upload
                        class="upload-demo"
                        action="https://jsonplaceholder.typicode.com/posts/"
                        :limit="1"
                        :on-change="handleUploadChange1"
                    >
                        <el-button type="primary">Click to upload</el-button>
                    </el-upload>
                </el-form-item>
            </el-tooltip>
            <el-tooltip class="box-item"
                        effect="dark"
                        content=".sql file to insert data into public database"
                        placement="top-start">
                <el-form-item label="Public dataset">
                    <el-upload
                        class="upload-demo"
                        action="https://jsonplaceholder.typicode.com/posts/"
                        :limit="1"
                        :on-change="handleUploadChange2"
                    >
                        <el-button type="primary">Click to upload</el-button>
                    </el-upload>
                </el-form-item>
            </el-tooltip>
            <el-tooltip class="box-item"
                        effect="dark"
                        content=".sql file to insert data into private database"
                        placement="top-start">
                <el-form-item label="Private dataset">
                    <el-upload
                        class="upload-demo"
                        action="https://jsonplaceholder.typicode.com/posts/"
                        :limit="1"
                        :on-change="handleUploadChange3"
                    >
                        <el-button type="primary">Click to upload</el-button>
                    </el-upload>
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
const deadline = ref('')
// do not use same name with ref
const descendent = ref(true)

const form = reactive({
    name: '',
    description: '',
    upload_limit:'',
    concurrent_limit: 1,
    running_time_limit:''
})

const onSubmit = () => {
    console.log('submit!')
    console.log(form.name)
    console.log(form.description)
    console.log(form.upload_limit)
    console.log(form.concurrent_limit)
    console.log(form.running_time_limit)
    console.log(deadline.value)
    console.log(descendent.value)
    console.log(reader)
    console.log(reader1)
    console.log(reader2)
    console.log(reader3)
    postCompetitionApi(form.name, form.description, form.upload_limit, form.concurrent_limit,
        form.running_time_limit, deadline.value, descendent.value, reader.result, reader1.result, reader2.result, reader3.result).then(() => {})
}

const reader = new FileReader()
const reader1 = new FileReader();
const reader2 = new FileReader();
const reader3 = new FileReader();

const competitorsFileList = []



const beforeUpload = (file) => {
    const fileType = file.name.substring(file.name.lastIndexOf('.'))
}

const uploadHttpRequest = (data) => {
    let reader = new FileReader()
    let that = this
    reader.readAsText(data.file)
    /*reader.onload = function() {
        that.formData.mmiapXml = this.result
    }*/
}

const handleUploadChange = (file) => {
    console.log(typeof file)
    console.log(file)
    reader.readAsBinaryString(file.raw)
}

const handleUploadChange1 = (file) => {
    console.log(typeof file)
    console.log(file)
    reader1.readAsBinaryString(file.raw)
}

const handleUploadChange2 = (file) => {
    console.log(file)
    reader2.readAsBinaryString(file.raw)
}

const handleUploadChange3 = (file) => {
    console.log(file)
    reader3.readAsBinaryString(file.raw)
}

const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
    console.log(file, uploadFiles)
}

const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
    console.log(uploadFile)
}

const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
    ElMessage.warning(
        `The limit is 1, you selected ${files.length} files this time, add up to ${
            files.length + uploadFiles.length
        } totally`
    )
}

const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
    return ElMessageBox.confirm(
        `Cancel the transfert of ${uploadFile.name} ?`
    ).then(
        () => true,
        () => false
    )
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