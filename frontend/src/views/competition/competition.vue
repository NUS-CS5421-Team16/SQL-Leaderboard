<template>
    <div style="padding: 50px" v-loading="loading">
        <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
            <el-tab-pane label="Competition Info" name="first">
                <el-table :data="table" style="width: 100%">
                    <el-table-column prop="name" label="Name" width="130" />
                    <el-table-column prop="deadline" label="Deadline" width="230" />
                    <el-table-column prop="upload_limit" label="Upload Limit" width="130"/>
                    <el-table-column prop="running_time_limit" label="Running Time Limit" width="180"/>
                    <el-table-column prop="concurrent_limit" label="Concurrent Limit" width="130"/>
                    <el-table-column prop="ordering" label="Ordering" width="130"/>
                    <el-table-column prop="description" label="Description" width="300"/>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="Update Competition" name="third"  v-if="has_competition==true&&role=='administrator'">
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
                            :placeholder="deadlinePlaceholder"
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
                    <el-button type="primary" @click="onUpdate">
                        Update
                    </el-button>
                </el-row>
            </el-tab-pane>
            <el-tab-pane label="Create Competition" name="second" v-if="has_competition==false&&role=='administrator'">
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
                            :placeholder="deadlinePlaceholder"
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
                    <el-button type="primary" @click="onSubmit">
                        Create
                    </el-button>
                </el-row>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script lang="ts">
import {defineComponent, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox, ElNotification} from "element-plus";
import {postCompetitionApi, getCompetitionApi, putCompetitionApi} from "@/api/competition";
import store from "@/store";

export default defineComponent ({
    inject:['reload'],
    methods: {
        getFile(target:any) {
            switch (target) {
                case "reference_query":
                    this.formData.append("reference_query", (<HTMLInputElement>document.getElementById("reference_query")).files[0])
                    break
                case "competitor_info":
                    this.formData.append("competitor_info", (<HTMLInputElement>document.getElementById("competitor_info")).files[0])
                    break
                case "public_sql":
                    this.formData.append("public_sql",  (<HTMLInputElement>document.getElementById("public_sql")).files[0])
                    break
                case "private_sql":
                    this.formData.append("private_sql", (<HTMLInputElement>document.getElementById("private_sql")).files[0])
                    break
                default:
                    break
            }
        },
        onUpdate() {
            this.formData.append("name", this.form.name)
            this.formData.append("description", this.form.description)
            this.formData.append("upload_limit", this.form.upload_limit)
            this.formData.append("concurrent_limit", this.form.concurrent_limit.toString())
            this.formData.append("running_time_limit", this.form.running_time_limit)
            this.formData.append("end_time", this.deadline)
            if (this.descendent) {
                this.formData.append("descendent_ordering", "true")
            } else {
                this.formData.append("descendent_ordering", "false")
            }
            this.loading = true
            putCompetitionApi(this.formData).then((res:any) => {
                if (res.id != null) {
                    this.has_competition = true
                    getCompetitionApi().then((res:any) => {
                        if (res.id != null) {
                            console.log("competitor_info: " + res.competitor_info)
                            console.log("reference_query: " + res.reference_query)
                            console.log("private_sql: " + res.private_sql)
                            console.log("public_sql: " + res.public_sql)
                            this.form.name = res.name
                            this.form.concurrent_limit = res.concurrent_limit
                            this.form.description = res.description
                            this.form.running_time_limit = res.running_time_limit
                            this.form.upload_limit = res.upload_limit
                            console.log("desc: " + res.descendent_ordering)
                            if (res.descendent_ordering) {
                                this.descendent = true
                            } else {
                                this.descendent = false
                            }
                            this.deadlinePlaceholder = res.end_time
                            this.has_competition = true
                            this.tableData.name = res.name
                            this.tableData.concurrent_limit = res.concurrent_limit
                            this.tableData.description = res.description
                            this.tableData.running_time_limit = res.running_time_limit
                            this.tableData.upload_limit = res.upload_limit
                            if (res.descendent_ordering) {
                                this.tableData.ordering = "descendent"
                            } else {
                                this.tableData.ordering = "ascendant"
                            }
                            this.tableData.deadline = res.end_time
                            this.table.push(this.tableData)
                            console.log("role: " + this.role)
                        } else {
                            this.role = "administrator"
                        }
                    })
                    ElNotification({
                        title: 'Success',
                        message: 'Update competition successfully',
                        type: 'success',
                        duration: 1500
                    })
                    this.loading = false
                    this.role = "administrator"
                    this.activeName = "third"
                    //this.$router.push({path: "/competition-admin"})
                } else {
                    ElNotification({
                        title: 'Error',
                        message: 'Update competition failed',
                        type: 'error',
                        duration: 1500
                    })
                    this.loading = false
                    this.role = "administrator"
                }
            })
        },
        onSubmit() {
            this.formData.append("name", this.form.name)
            this.formData.append("description", this.form.description)
            this.formData.append("upload_limit", this.form.upload_limit)
            this.formData.append("concurrent_limit", this.form.concurrent_limit.toString())
            this.formData.append("running_time_limit", this.form.running_time_limit)
            this.formData.append("end_time", this.deadline)
            if (this.descendent) {
                this.formData.append("descendent_ordering", "true")
            } else {
                this.formData.append("descendent_ordering", "false")
            }
            this.loading = true
            postCompetitionApi(this.formData).then((res:any) => {
                if (res.id != null) {
                    this.has_competition = true
                    this.role = "administrator"
                    getCompetitionApi().then((res:any) => {
                        if (res.id != null) {
                            console.log("competitor_info: " + res.competitor_info)
                            console.log("reference_query: " + res.reference_query)
                            console.log("private_sql: " + res.private_sql)
                            console.log("public_sql: " + res.public_sql)
                            this.form.name = res.name
                            this.form.concurrent_limit = res.concurrent_limit
                            this.form.description = res.description
                            this.form.running_time_limit = res.running_time_limit
                            this.form.upload_limit = res.upload_limit
                            console.log("desc: " + res.descendent_ordering)
                            if (res.descendent_ordering) {
                                this.descendent = true
                            } else {
                                this.descendent = false
                            }
                            this.deadlinePlaceholder = res.end_time
                            this.has_competition = true
                            this.tableData.name = res.name
                            this.tableData.concurrent_limit = res.concurrent_limit
                            this.tableData.description = res.description
                            this.tableData.running_time_limit = res.running_time_limit
                            this.tableData.upload_limit = res.upload_limit
                            if (res.descendent_ordering) {
                                this.tableData.ordering = "descendent"
                            } else {
                                this.tableData.ordering = "ascendant"
                            }
                            this.tableData.deadline = res.end_time
                            this.table.push(this.tableData)
                            console.log("role: " + this.role)
                        } else {
                            this.role = "administrator"
                        }
                    })
                    ElNotification({
                        title: 'Success',
                        message: 'Create competition successfully',
                        type: 'success',
                        duration: 1500
                    })
                    this.loading = false
                    this.role = "administrator"
                    this.activeName = "third"
                    //this.$router.push({path: "/competition-admin"})
                } else {
                    this.role = "administrator"
                    ElNotification({
                        title: 'Error',
                        message: 'A competition already exist',
                        type: 'error',
                        duration: 1500
                    })
                    this.loading = false
                    this.role = "administrator"
                }
            })
        },
        handleClick(tab, event){
            console.log(tab, event)
        }
    },
    data() {
        return {
            deadline: '',
            descendent: true,
            form: {
                name: '',
                description: '',
                upload_limit:'',
                concurrent_limit: 1,
                running_time_limit:'',
            },
            formData: new FormData(),
            loading: false,
            deadlinePlaceholder: "Select date and time",
            has_competition: false,
            tableData: {
                name: '',
                deadline: '',
                upload_limit: '',
                running_time_limit: '',
                concurrent_limit: '',
                ordering: '',
                description: ''
            },
            table: [],
            createDialog: false,
            updateDialog: false,
            activeName: "first",
            role: ""
        }
    },
    created() {
        this.role = store.getters.getRole
        console.log("current role: " + this.role)
        console.log("current has competition: " + this.has_competition)
        getCompetitionApi().then((res:any) => {
            if (res.id != null) {
                console.log("competitor_info: " + res.competitor_info)
                console.log("reference_query: " + res.reference_query)
                console.log("private_sql: " + res.private_sql)
                console.log("public_sql: " + res.public_sql)
                this.form.name = res.name
                this.form.concurrent_limit = res.concurrent_limit
                this.form.description = res.description
                this.form.running_time_limit = res.running_time_limit
                this.form.upload_limit = res.upload_limit
                console.log("desc: " + res.descendent_ordering)
                if (res.descendent_ordering) {
                    this.descendent = true
                } else {
                    this.descendent = false
                }
                this.deadlinePlaceholder = res.end_time
                this.has_competition = true
                this.tableData.name = res.name
                this.tableData.concurrent_limit = res.concurrent_limit
                this.tableData.description = res.description
                this.tableData.running_time_limit = res.running_time_limit
                this.tableData.upload_limit = res.upload_limit
                if (res.descendent_ordering) {
                    this.tableData.ordering = "descendent"
                } else {
                    this.tableData.ordering = "ascendant"
                }
                this.tableData.deadline = res.end_time
                this.table.push(this.tableData)
                console.log("role: " + this.role)
            } else {
                this.role = "administrator"
            }
        })
    }
})
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